# -*- coding: utf-8 -*-

from odoo import models, fields, api


class cam_sector(models.Model):
    _name = 'cam.sector'
    _description = 'cam.sector'


    name = fields.Char("Nombre")


    function_ids = fields.Many2many(comodel_name='cam.function',relation="cam_sector_function", 
                                                 column2="sector_id",column1="function_id",
                                                 string="Funciones")

