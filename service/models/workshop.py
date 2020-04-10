# -*- coding: utf-8 -*-

from odoo import models, fields, api


class vehicle(models.Model):
    _name = 'cam.workshop'
    _description = 'cam.workshop'


    name = fields.Char("Nombre")

    operation_base_id = fields.Many2one("cam.operation_base","Base de operaciones")

    def display_name(self):
        for rec in self:
            name = rec.name if rec.name else "" 
            operation_base = " - " + rec.operation_base_id.display_name if rec.operation_base_id.display_name else ""
            
            rec.display_name = name + operation_base


    display_name = fields.Char(compute=display_name)
