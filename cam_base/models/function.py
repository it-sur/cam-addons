# -*- coding: utf-8 -*-

from odoo import models, fields, api


class vehicle(models.Model):
    _name = 'cam.function'
    _description = 'cam.function'


    name = fields.Char("Nombre")
    
    sector_ids = fields.Many2many(comodel_name='cam.sector',relation="cam_sector_function", 
                                                 column1="sector_id",column2="function_id",
                                                 string="Sectores")

    
    #
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
