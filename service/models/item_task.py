# -*- coding: utf-8 -*-

from odoo import models, fields, api


class item_task(models.Model):
    _name = 'cam.item_task'
    _description = 'cam.item_task'

    workshop_id = fields.Many2one("cam.workshop",string="Taller")
    mechanic_id = fields.Many2one("cam.mechanic",string="Mecanico")
    progress = fields.Selection([("charged","Cargada"),
                              ("assigned","Asignada"),
                              ("in_progress","En Progreso"),
                              ("paused","En Pausa")
                              ("finalized","Finalizada"),
                              ],
                                    string="Estado de progreso",required="True",default='charged')
    
    progress_percentage = fields.Float("% de avance")
    
    type = fields.Selection([("planned","Planificada"),
                               ("extra","Extra/diagnostico"),
                               ("third_party","Tercero"),
                               ],
                               string="Tipo",required="True",default='planned')

    result = fields.Selection([("solved","Solucionado"),
                               ("not_solved","No solucionado"),
                               ("incomplete","Incompleto"),
                               ("pending","Pendiente"),
                               ],
                               string="Estado de progreso",required="True",default='charged')

    result_description = fields.Text("Motivo del Resultado")

    estimated_time = fields.Integer("Tiempo estimado (min)")

    time_lapse_ids = fields.One2many("item_task",string="Tiempo empleado") 

    task_id = fields.Many2one("cam.task",string="Tarea")
    description = fields.Char(related="task_id.description")

    

