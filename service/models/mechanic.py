# -*- coding: utf-8 -*-

from odoo import models, fields, api


class mechanic(models.Model):
    _name = 'cam.mechanic'
    _description = 'cam.mechanic'

    _inherits = {'hr.employee': 'hr_employee_id'}


    hr_employee_id = fields.Many2one(
        'hr.employee', 'Empleado',
        delegate=True, required=True, ondelete='restrict')


    workshop_id = fields.Many2one("cam.workshop")