# -*- coding: utf-8 -*-

from odoo import models, fields, api


class operation_base(models.Model):
    _name = 'cam.operation_base'
    _description = 'cam - base de operaciones'


    name = fields.Char("Nombre")
    code = fields.Char("Codigo")

