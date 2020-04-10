# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class vehicle(models.Model):
    _inherit = ["cam.vehicle"]
    
    service_ids = fields.One2many(comodel_name="cam.service",inverse_name="vehicle_id",string="Servicios")

    related_tool_id = fields.Many2one('cam.tool',string="Herramienta",compute='_compute_tool')


    def _compute_tool(self):
        for rec in self:
            result = self.env['cam.tool'].search([('owner_vehicle_id','=',rec.id)])
            if len(result)==1:
                rec.related_tool_id = result[0]
