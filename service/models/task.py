# -*- coding: utf-8 -*-

from odoo import models, fields, api


class task(models.Model):
    _name = 'cam.task'
    _description = 'cam.task'

    name = fields.Char("Nombre")
    description = fields.Char("Descripcion de la tarea")

    brand_id = fields.Many2one("cam.brand")
    model_id = fields.Many2one("brand_id.model_id")

#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
