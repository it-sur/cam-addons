# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class maintainable_object(models.Model):
    _name = 'cam.maintainable_object'
    _description = 'cam.maintainable_object'
    _inherit = ['image.mixin']


    def _get_states(self):
        return [("working", "Operativo"),
                               ("working_but", "Operativo pero observado"),
                               ("out_of_service", "Fuera de servicio"),
                               ("sold", "Vendido"),
                               ]

    create_date = fields.Datetime("Fecha de carga", readonly=True)
    
    acquisition_date = fields.Date("Fecha de compra")
   
    photos_ids = fields.Many2many('ir.attachment', string='Imagenes')


    state = fields.Selection(_get_states, default="working",
                              string="Estado", required=True)



    
