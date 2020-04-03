# -*- coding: utf-8 -*-

from odoo import models, fields, api


class person(models.Model):
    #_name = 'cam.person'
    _description = 'cam.person'

    _inherit = 'res.partner'

    """
    @api.model
    def default_get(self, fields):
        context = self._context or {}
        res = super(person, self).default_get(fields)

        if ('supplier' in fields) & (bool(context.get("supplier")) == True):
            res.update({'supplier': True})
            res.update({'customer': False})
        if ('customer' in fields) & (bool(context.get("customer")) == True):
            res.update({'supplier': False})
            res.update({'customer': True})
        if ('employee' in fields) & (bool(context.get("employee")) == True):
            res.update({'employee': True})
        
        return res
    """
    
    @api.onchange('name')
    def onchange_name(self):
        if self.name:
            self.name = self.name.title()
        