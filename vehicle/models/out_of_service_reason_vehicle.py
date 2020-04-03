# -*- coding: utf-8 -*-

from odoo import models, fields, api


class out_of_service_reason_vehicle(models.Model):
    _name = 'cam.out_of_service_reason_vehicle'
    _description = 'cam.out_of_service_reason_vehicle'
    _inherit = ['image.mixin']


    starttime = fields.Datetime("Fecha y hora inicio")
    endtime = fields.Datetime("Fecha y hora fin")
    short_description = fields.Char("Descripcion corta")
    long_description = fields.Text("Comentarios")

    reason = fields.Char("Motivo")
    
    vehicle_id = fields.Many2one("cam.vehicle")