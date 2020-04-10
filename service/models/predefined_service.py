# -*- coding: utf-8 -*-

from odoo import models, fields, api


class predefined_service(models.Model):
    _name = 'cam.predefined_service'
    _description = 'cam.predefined_service'


    name = fields.Char("Nombre")
    
    
    task_planned_ids = fields.Many2many(comodel_name="cam.task",relation="cam_predefined_service_task_planned",column1="predefined_service_id",column2="task_planned_id"
                                              ,string="Tareas Planificadas")# readonly for user
