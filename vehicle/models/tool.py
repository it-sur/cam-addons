# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class tool(models.Model):
    _name = 'cam.tool'
    _description = 'cam.tool'
    
    _inherit = ["cam.maintainable_object"]

    nro_serie = fields.Char("Nro Serie", track_visibility='onchange')

    engine_id = fields.Many2one("cam.engine",string="Motor")


    brand_id = fields.Many2one(related="model_id.brand_id", string="Marca", track_visibility='onchange')
    model_id = fields.Many2one("cam.tool_model", string="Modelo", track_visibility='onchange')


    out_of_service_reason_ids = fields.One2many(comodel_name='cam.out_of_service_reason_tool',inverse_name="tool_id",
                                                 string='Razones de fuera de servicio')
    
