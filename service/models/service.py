# -*- coding: utf-8 -*-

from odoo import models, fields, api


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


    name = fields.Char("Nombre", readonly=True)

    datetime_programmed = fields.Datetime("Fecha y hora programada")
    
    mantainable_object_id = fields.Many2one("cam.mantainable_object",string="Vehiculo/Herramienta",domain=[("_name","=","cam.vehicle")]) #Vehiculo, Herramienta.
    workshop_id = fields.Many2one("cam.workshop",string="Taller")

    mechanic_id = fields.Many2one("res.partner",string="Mecanico")

    service_type = fields.Selection(_get_service_types, default="preventive",
                              string="Tipo de servicio", required=True)    
    
    service_sub_type = fields.Selection(_get_service_sub_types, default="corrective_default",
                              string="Tipo de servicio", required=True)    
    
    diagnostics = fields.Text("Diagnostico")

    predefined_service_id = fields.Many2one("cam.predefined_service",string="Servicio Predefinido")
    
    task_planned_ids = fields.One2many(comodel_name="cam.item_task",inverse_name="service_id",domain=[('','','')],string="Tareas Planificadas")# readonly for user
    
    task_diagnostics_ids = fields.One2many(comodel_name="cam.item_task",inverse_name="service_id",domain=[('','','')],string="Tareas extras/diagnósticas") # recolectado cuando llega el camion
    
    third_work_ids = fields.One2many(comodel_name="cam.item_task",inverse_name="service_id",domain=[('','','')],string="Trabajo de tercero") #trabajo de tercero por ahora como item
    
