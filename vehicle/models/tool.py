# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class tool(models.Model):
    _name = 'cam.tool'
    _description = 'cam.tool'
    
    _inherit = ["cam.maintainable_object"]


    def display_name(self):
        for rec in self:
            serie = rec.nro_serie if rec.nro_serie else "" 
            marca = ""
            if rec.brand_id:
                marca = " - "+ rec.brand_id.display_name  if rec.brand_id.display_name else ""
            estado = ""
            if rec.state:
            
                estado = "(" + [item for item in rec._get_states() if item[0] == rec.state][0][1] + ")"
            
            rec.display_name = serie + marca + estado


    display_name = fields.Char(compute=display_name)

    owner_vehicle_id = fields.Many2one("cam.vehicle",string="Vehiculo")

    brand_id = fields.Many2one(related="model_id.brand_id", string="Marca", track_visibility='onchange')
    model_id = fields.Many2one("cam.tool_model", string="Modelo", track_visibility='onchange')


    out_of_service_reason_ids = fields.One2many(comodel_name='cam.out_of_service_reason_tool',inverse_name="tool_id",
                                                 string='Razones de fuera de servicio')
    
