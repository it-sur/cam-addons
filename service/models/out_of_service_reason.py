# -*- coding: utf-8 -*-

from odoo import models, fields, api


class out_of_service_reason(models.Model):

    _name = "cam.out_of_service_reason"
    _description = "cam.out_of_service_reason"

    
    
    name = fields.Char(string="Descripcion")
    
    service_id = fields.Many2one("cam.service",string="Servicio relacionado")
    
    def display_name(self):
        for rec in self:
            name = rec.name if rec.name else ""
            service = ""
            if rec.workshop_id:
                service = " [" + rec.service_id.display_name +"]" if rec.service_id.display_name else ""
            
            
            rec.display_name = ''.join([name, service])


    display_name = fields.Char(compute=display_name)
    
    