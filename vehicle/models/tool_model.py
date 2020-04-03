# -*- coding: utf-8 -*-

from odoo import models, fields, api


class tool_model(models.Model):
    _name = 'cam.tool_model'
    _description = 'cam.tool_model'

    name = fields.Char(string="Nombre")
    
    description = fields.Char(string="Descripción")

    brand_id = fields.Many2one("cam.brand", string="Marca", track_visibility='onchange',domain=[('brand_type','=','tool')])

    
