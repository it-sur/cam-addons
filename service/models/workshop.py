# -*- coding: utf-8 -*-

from odoo import models, fields, api


class vehicle(models.Model):
    _name = 'cam.workshop'
    _description = 'cam.workshop'


    name = fields.Char("Nombre")


#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
