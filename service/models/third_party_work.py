# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class third_party_work(models.Model):
    _name = 'cam.third_party_work'
    _description = 'cam.third_party_work'


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
    
    res_partner_id = fields.Many2one("res.partner",string="Tercero")
    """
                                    change_default=True, tracking=True, 
                                    domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")"""
    def _get_states(self):
        return [("charged","Cargada"),
                              ("in_progress","En Progreso"),
                              ("finalized","Finalizada")
                              ]
   
    state = fields.Selection(_get_states,default='charged',
                                    string="Estado de progreso",required="True")
    
    def _get_result(self):
        return [("solved","Solucionado"),
                               ("not_solved","No solucionado"),
                               ("incomplete","Incompleto"),
                               ("pending","Pendiente"),
                               ]
    
    result = fields.Selection(_get_result,
                               string="Resultado")

    result_description = fields.Text("Motivo del Resultado")


    service_id = fields.Many2one("cam.service",string="Servicio",required=True, readonly=True)

    task = fields.Char(string="Tarea",required=True)

    start_time = fields.Datetime("Fecha inicio")
    end_time = fields.Datetime("Fecha fin")


    def start(self):
        for rec in self:
            if ( (rec.service_id.state == 'finished') | (rec.service_id.state == 'finished_but')):
                raise ValidationError('No se puede iniciar una tarea si el servicio esta cerrado')
            
            rec.state = 'in_progress'
            if not(rec.start_time):
                rec.start_time = fields.Datetime.now()
            rec.service_id._compute_times()
        #create elapsed time
        #set start_time
        print('start')

    def stop(self):
        for rec in self:
            rec.state = 'finalized'
            rec.end_time = fields.Datetime.now()
            rec.service_id._compute_times()
        print('stop')


