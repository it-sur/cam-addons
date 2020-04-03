# -*- coding: utf-8 -*-

from odoo import models, fields, api


class model(models.Model):
    _name = 'cam.vehicle_model'
    _description = 'cam.vehicle_model'

    name = fields.Char(string="Nombre")
    
    description = fields.Char(string="Descripción")

    vehicle_type = fields.Selection([("car","Auto"),("pickup","Pickup"),("truck","Camión")],
                                    string="Tipo",required="True",default='truck')

    brand_id = fields.Many2one("cam.brand", string="Marca", track_visibility='onchange',domain=[('brand_type','=','vehicle')])

    seats = fields.Integer("Asientos")
    doors = fields.Integer("Puertas")
    color = fields.Char("Puertas")
    model_year = fields.Integer("Anio del modelo")


    _sql_constraints = [
            ('vehicle_model_name_unique', 'unique(name)', 'El nombre debe ser único'),
    ]
    
