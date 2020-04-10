# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class item_task(models.Model):
    _name = 'cam.item_task'
    _description = 'cam.item_task'


    def display_name(self):
        for rec in self:
            task = ""
            if rec.task_id:
                task = rec.task_id.display_name if rec.task_id.display_name else ""
            
            workshop = ""
            if rec.workshop_id:
                workshop = "/" + rec.workshop_id.display_name + "/" if rec.workshop_id.display_name else ""
                
            progress_percentage = "("+str(rec.progress_percentage)+"%)" if rec.progress_percentage else ""
            
            rec.display_name = ''.join([task, workshop, progress_percentage])


    display_name = fields.Char(compute=display_name)
    

    mechanic_id = fields.Many2one("cam.mechanic",string="Mecanico")
    workshop_id = fields.Many2one(realted="mechanic_id.workshop_id",string="Taller")
    
    
    def _get_states(self):
        return [("charged","Cargada"),
                              ("assigned","Asignada"),
                              ("in_progress","En Progreso"),
                              ("paused","En Pausa"),
                              ("finalized","Finalizada")
                              ]
   
    @api.depends('mechanic_id')
    @api.onchange('mechanic_id')
    def check_is_assigned(self):
        res = []
        for rec in self:
            if rec.mechanic_id:
                rec.state = 'assigned'
            else:
                rec.state = 'charged'
            res.append((rec.id,rec.state))   
       
   
    state = fields.Selection(_get_states,
                                    string="Estado de progreso",required="True",default=check_is_assigned)
    
    progress_percentage = fields.Percent("% de avance",readonly=True)
    
    over_under_work = fields.Integer("Exceso/Ahorro de trabajo")
    
    def _get_type(self):
        return [("planned","Planificada"),
                               ("extra","Extra/diagnostico"),
                               ]
    
    type = fields.Selection(_get_type,
                               string="Tipo",required="True")

    def _get_result(self):
        return [("solved","Solucionado"),
                               ("not_solved","No solucionado"),
                               ("incomplete","Incompleto"),
                               ("pending","Pendiente"),
                               ]
    
    result = fields.Selection(_get_result,
                               string="Resultado")

    result_description = fields.Text("Motivo del Resultado")


    elapsed_time_ids = fields.One2many("cam.elapsed_time","item_task_id",string="Tiempo empleado",readonly=True) 
    
    service_id = fields.Many2one("cam.service",string="Servicio",required=True, readonly=True)

    task_id = fields.Many2one("cam.task",string="Tarea",required=True)

    start_time = fields.Datetime("Fecha inicio",compute="_compute_times",readonly=True)
    end_time = fields.Datetime("Fecha fin",compute="_compute_times",readonly=True)
    estimated_time = fields.Integer(related="task_id.estimated_time",readonly=True)
    elapsed_time = fields.Integer(string="tiempo empleado (min)",compute="_compute_times",readonly=True)


    @api.depends('elapsed_time_ids','elapsed_time_ids.start_time','elapsed_time_ids.end_time','elapsed_time_ids.elapsed_time')
    @api.onchange('elapsed_time_ids')
    def _compute_times(self):
        for rec in self:
            elap_time = 0
            
            start_time = rec.start_time
            end_time = rec.end_time
            
            for etime in rec.elapsed_time_ids:
                elap_time += etime.elapsed_time
                
                if bool(etime.start_time):
                    if bool(start_time):
                        if etime.start_time < start_time:
                            start_time = etime.start_time
                    else:
                        start_time = etime.start_time
                if bool(etime.end_time):
                    if bool(end_time):
                        if etime.end_time > end_time:
                            end_time = etime.end_time
                    else:
                        end_time = etime.end_time
                        
            rec.start_time = start_time
            rec.end_time = end_time
    
            rec.elapsed_time = elap_time
        
            estimated = rec.estimated_time
            elapsed = rec.elapsed_time
            if estimated>elapsed:
                rec.progress_percentage = elap_time * 100 / estimated
            else:
                rec.progress_percentage = 100
                
            
            if rec.state == 'finalized': 
                rec.over_under_work = elap_time - estimated
                rec.progress_percentage = 100
                


    def start(self):
        for rec in self:
            if ( (rec.service_id.state == 'finished') | (rec.service_id.state == 'finished_but')):
                raise ValidationError('No se puede iniciar una tares si el servicio esta cerrado')
            
            elap_time = self.env['cam.elapsed_time'].create({'item_task_id':rec.id})
            rec.state = 'in_progress'
            rec._compute_times()
            rec.service_id._compute_times()
        #create elapsed time
        #set start_time
        print('start')

    def stop(self):
        for rec in self:
            for et in rec.elapsed_time_ids:
                if not (et.end_time):
                    et.end_time = fields.Datetime.now()
            rec.state = 'paused'
            rec._compute_times()
            rec.service_id._compute_times()
        print('stop')
    
    def continue_task(self):
        for rec in self:
            if ( (rec.service_id.state == 'finished') | (rec.service_id.state == 'finished_but')):
                raise ValidationError('No se puede iniciar una tares si el servicio esta cerrado')
            
            
            elap_time = self.env['cam.elapsed_time'].create({'item_task_id':rec.id})
            rec.state = 'in_progress'
            rec._compute_times()
            rec.service_id._compute_times()
        print('continue')
    
    def end(self,itwf):
        for rec in self:
            for et in rec.elapsed_time_ids:
                if not (et.end_time):
                    et.end_time = fields.Datetime.now()
            rec.state = 'finalized'
            rec.result = itwf.result
            rec.result_description = itwf.result_description
            itwf.unlink()
            rec._compute_times()
            rec.service_id._compute_times()
        print('end')


