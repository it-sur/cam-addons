# -*- coding: utf-8 -*-

from odoo import models, fields, api


class item_task(models.Model):
    _name = 'cam.time_lapse'
    _description = 'cam.time_lapse'

    start_time = fields.Datetime("Fecha hora de Inicio")
    end_time = fields.Datetime("Fecha Hora de fin")
    
    elapsed_time = fields.Integer("Tiempo empleado")
    
    item_task = fields.Many2one("cam.item_task")