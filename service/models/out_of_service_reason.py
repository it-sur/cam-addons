# -*- coding: utf-8 -*-

from odoo import models, fields, api


class out_of_service_reason(models.Model):

    _inherit = "cam.out_of_service_reason"

    service_id = fields.Char("cam.service",string="Servicio relacionado")
    
