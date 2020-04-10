# -*- coding: utf-8 -*-

from odoo import models, fields, api


class elapsed_time(models.Model):
    _name = 'cam.elapsed_time'
    _description = 'cam.elapsed_time'

    start_time = fields.Datetime("Fecha hora de Inicio",default=fields.Datetime.now)
    end_time = fields.Datetime("Fecha Hora de fin")
    
    elapsed_time = fields.Integer("Tiempo empleado",compute="_compute_time",readonly=True)
    
    item_task_id = fields.Many2one("cam.item_task")
    
    @api.depends('end_time')
    def _compute_time(self):
        for rec in self:
            if rec.end_time:
                time = rec.end_time - rec.start_time
                rec.elapsed_time = time.days*24*60+time.seconds/60
            else:
                time = fields.Datetime.now() - rec.start_time
                rec.elapsed_time = time.days*24*60+time.seconds/60
        
