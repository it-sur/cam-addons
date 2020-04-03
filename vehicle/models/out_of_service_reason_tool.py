# -*- coding: utf-8 -*-

from odoo import models, fields, api


class out_of_service_reason_tool(models.Model):
    _name = 'cam.out_of_service_reason_tool'
    _description = 'cam.out_of_service_reason_tool'
    _inherit = ['image.mixin']


    starttime = fields.Datetime("Fecha y hora inicio")
    endtime = fields.Datetime("Fecha y hora fin")
    short_description = fields.Char("Descripcion corta")
    long_description = fields.Text("Comentarios")

    reason = fields.Char("Motivo")
    
    tool_id = fields.Many2one("cam.tool")