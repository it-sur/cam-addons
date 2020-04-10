# -*- coding: utf-8 -*-

from odoo import models, fields, api


class task(models.Model):
    _name = 'cam.task'
    _description = 'cam.task'

    name = fields.Char("Nombre")
    description = fields.Char("Descripcion de la tarea")

    estimated_time = fields.Integer("Tiempo estimado (min)")

