# -*- coding: utf-8 -*-

from odoo import models, fields, api


class brand(models.Model):
    _name = 'cam.brand'
    _description = 'cam.brand'


    name = fields.Char(string="Nombre")

    brand_type = fields.Selection([("vehicle","Vehículo"),("tool","Herramienta"),("other","Otra")],
                                    string="Tipo de marca",required="True",default='vehicle')

