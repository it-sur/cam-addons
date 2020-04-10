# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class serice(models.Model):
    _name = 'cam.service'
    _description = 'cam.service'


    def _get_service_sub_types(self):
        return [("corrective_default", "Correctivo Natural"),
                               ("corrective_human", "Correctivo accidente o negligencia"),
                               ]
    def _get_service_types(self):
        return [("preventive", "Preventivo"),
                               ("corrective", "Correctivo"),
                               ]


    def _compute_service_type_subtype(self):
        for rec in self:
            try:
                type_s_value = [item for item in rec._get_service_types() if item[0] == rec.service_type][0][1]
                type_st_value = [item for item in rec._get_service_sub_types() if item[0] == rec.service_sub_type][0][1]
                type_s = type_s_value if (type_s_value!=False) else ""
                if rec.service_type == 'corrective':
                    type_st = "("+type_st_value+")" if (type_st_value!=False) else ""
                else: type_st = ""
                rec.service_type_subtype = type_s + type_st
            except Exception as e:
                pass
        
    

    def open_service(self):
        for rec in self:
            if bool(rec.datetime_programmed):
                rec.state = 'in_progress'
                if not bool(rec.start_time):
                    rec.start_time = fields.Datetime.now()
                
                if not bool(rec.open_time):
                    rec.open_time = fields.Datetime.now()
                rec.close_time = False   
                
                rec.vehicle_id.state = 'out_of_service'
                
                self.env['cam.out_of_service_reason_vehicle'].create({
                    'starttime':rec.open_time,
                    'reason':rec.name,
                    'vehicle_id':rec.vehicle_id.id,
                    })
            else:
                pass # no hay que mostrar el boton si no hay fecha de programacion   
            
            
            
        
        
    def close_service(self):
        for rec in self:
            task_ids = rec.task_planned_ids | rec.task_diagnostics_ids
            
            observations = ""
            
            for t in task_ids:
                if not(t.state == 'finalized'):
                    raise ValidationError('No se puede cerrar el servicio. Hay tareas abiertas.')
                else:
                    if not(t.result == 'solved'):
                        observations +=  t.result_description + " / " 

            for tpw in rec.third_party_work_ids:
                if not(tpw.state == 'finalized'):
                    raise ValidationError('No se puede cerrar el servicio. Hay tareas de terceros abiertas.')
                else:
                    if not(tpw.result == 'solved'):
                        observations += tpw.result_description +" / " 

            rec.close_time = fields.Datetime.now()

            oosv = self.env['cam.out_of_service_reason_vehicle'].search([('vehicle_id','=',rec.vehicle_id.id),('endtime','=',False),('reason','=',rec.name)])

            if len(oosv) >0:
                oosv = oosv[0]
                oosv.endtime = rec.close_time                

            if observations == "":
                rec.state = 'finished'
            else:
                rec.state = 'finished_but'
                if observations not in rec.observation:
                    rec.observation += " // "+ observations
                oosv.long_description = rec.observation
                rec.vehicle_id.state = 'working_but'
                
            


    @api.depends('datetime_programmed')
    def change_state(self):
        for rec in self:
            if bool(rec.datetime_programmed) & (rec.state=='draft'):
                rec.state = 'programmed'
    
    def _get_states(self):
        return [("draft", "Borrador"),
               ("programmed", "Programado"),
               ("in_progress", "En Progreso"),
               ("finished", "Finalizado"),
               ("finished_but", "Finalizado con Observaciones")
               ]

    state = fields.Selection(_get_states,string="Estado",required=True,readonly=True,default="draft")




    def display_name(self):
        for rec in self:
            name = rec.name if rec.name else ""
            vehicle_nro_serie = ", "+rec.vehicle_nro_serie if rec.vehicle_nro_serie else ""
            workshop = ""
            if rec.workshop_id:
                workshop = ", " + rec.workshop_id.display_name if rec.workshop_id.display_name else ""
            
            predefined_service = ""
            if rec.predefined_service_id:
                predefined_service = "/" + rec.predefined_service_id.display_name + "/" if rec.predefined_service_id.display_name else ""
            state_name = ""
            if rec.state:
                state_name = "("+[item for item in rec._get_states() if item[0] == rec.state][0][1]+")"

            
            rec.display_name = ''.join([name, vehicle_nro_serie, workshop, predefined_service, state_name])


    display_name = fields.Char(compute=display_name)
    
    name = fields.Char("Nombre")
    

    datetime_programmed = fields.Datetime("Fecha y hora programada")

    related_service_id = fields.Many2one("cam.service",string="Servicio Relacionado")
    related_service_observation = fields.Text(related="related_service_id.observation")
    
    vehicle_id = fields.Many2one("cam.vehicle",string="Vehiculo")#,domain=[("_name","=","cam.vehicle")]) #Vehiculo, Herramienta.
    vehicle_nro_serie = fields.Char(related="vehicle_id.nro_serie")
    vehicle_model_id = fields.Many2one(related="vehicle_id.model_id")
    vehicle_patent = fields.Char(related="vehicle_id.patent")
    vehicle_sector_id = fields.Many2one(related="vehicle_id.sector_id")
    vehicle_function_id = fields.Many2one(related="vehicle_id.function_id")
    vehicle_engine_id = fields.Many2one(related="vehicle_id.engine_id")

    vehicle_related_tool_id = fields.Many2one(related="vehicle_id.related_tool_id")

    workshop_id = fields.Many2one("cam.workshop",string="Taller")

    service_type = fields.Selection(_get_service_types, default="preventive",
                              string="Tipo de servicio", required=True)    
    
    service_sub_type = fields.Selection(_get_service_sub_types, default="corrective_default",
                              string="Tipo de servicio", required=True)    


    service_type_subtype = fields.Char(string="Tipo de servicio",compute="_compute_service_type_subtype")
    
    diagnostics = fields.Text("Diagnostico")
    
    observation = fields.Text("Observaciones")




    """
    Lanzar advertencia para borrar todas las tareas planeadas al cambiar este valor.
    """
    predefined_service_id = fields.Many2one("cam.predefined_service",string="Servicio Predefinido")
    
    
    task_planned_ids = fields.One2many(comodel_name="cam.item_task",inverse_name="service_id"
                                        ,domain=[('type','=','planned')]
                                        ,string="Tareas Planificadas")# readonly for user
    
    task_diagnostics_ids = fields.One2many(comodel_name="cam.item_task",inverse_name="service_id"
                                            ,domain=[('type','=','extra')]
                                            ,string="Tareas extras/diagnósticas") # recolectado cuando llega el camion
    
    third_party_work_ids = fields.One2many(comodel_name="cam.third_party_work",inverse_name="service_id",
                                           string="Trabajo de terceros")
    """
    third_party_work_ids = fields.One2many(comodel_name="cam.item_task",inverse_name="service_id"
                                      ,domain=[('type','=','third_party')]
                                      ,ondelete="CASCADE"
                                      ,string="Trabajo de tercero") #trabajo de tercero por ahora como item
    """
    
    open_time = fields.Datetime("Fecha de apertura",readonly=True)
    close_time = fields.Datetime("Fecha de cierre",readonly=True)
    
    start_time = fields.Datetime("Fecha/hora de inicio",compute="_compute_times",readonly=True,store=True)
    end_time = fields.Datetime("Fecha/hora de fin",compute="_compute_times",readonly=True,store=True)
    elapsed_time = fields.Float("Tiempo trabajado",compute="_compute_times",readonly=True)
    programmed_time = fields.Float("Tiempo programado",compute="_compute_times",readonly=True)
    
    
    @api.depends('predefined_service_id','task_planned_ids','task_diagnostics_ids','task_planned_ids.state','task_diagnostics_ids.state','third_party_work_ids')
    @api.onchange('predefined_service_id','task_planned_ids','task_diagnostics_ids','task_planned_ids.state','task_diagnostics_ids.state','third_party_work_ids')
    def _compute_times(self):
        
        for rec in self:
            item_task_ids = self.env['cam.item_task'].search([('service_id','=',rec.id)])
            third_party_work_ids = self.env['cam.third_party_work'].search([('service_id','=',rec.id)]) 
            elapsed_time = 0
            estimated_time = 0
            start_time = rec.start_time
            end_time = rec.end_time
            
            for itask in third_party_work_ids:
                if bool(itask.start_time):
                    if bool(start_time):
                        if itask.start_time < start_time:
                            start_time = itask.start_time
                    else:
                        start_time = itask.start_time
                if bool(itask.end_time):
                    if bool(end_time):
                        if itask.end_time < end_time:
                            end_time = itask.end_time
                    else:
                        end_time = itask.end_time
                        
            for itask in item_task_ids:
                elapsed_time += itask.elapsed_time
                estimated_time += itask.estimated_time

                if bool(itask.start_time):
                    if bool(start_time):
                        if itask.start_time < start_time:
                            start_time = itask.start_time
                    else:
                        start_time = itask.start_time
                if bool(itask.end_time):
                    if bool(end_time):
                        if itask.end_time > end_time:
                            end_time = itask.end_time
                    else:
                        end_time = itask.end_time
            
            rec.start_time = start_time
            rec.end_time = end_time
            
            rec.elapsed_time = elapsed_time
            rec.programmed_time = estimated_time


    @api.depends('service_type')
    def clean_service_sub_type_if_required(self):
        for rec in self:
            if rec.service_type == 'preventive':
                rec.service_sub_type = ''
        