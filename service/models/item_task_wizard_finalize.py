# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class item_task_wizard_finalize(models.TransientModel):
    _name = 'cam.item_task_wizard_finalize'
    _description = 'cam.item_task_wizard_finalize'
    
    #_auto = False 
    _log_access = True # Include magic fields

    def _get_result(self):
        return [("solved","Solucionado"),
                               ("not_solved","No solucionado"),
                               ("incomplete","Incompleto"),
                               ("pending","Pendiente"),
                               ]
    
    result = fields.Selection(_get_result,
                               string="Estado de progreso",required=True)

    @api.constrains('result','result_description')
    def _if_result(self):
        for rec in self:
            if (rec.result == 'solved'): return 
            if not(rec.result_description):
                raise ValidationError('La descripcion debe ser completada si el resultado no es Solucionado')
            elif len(rec.result_description) < 5:
                raise ValidationError('La descripcion debe ser completada si el resultado no es Solucionado')
                 

    result_description = fields.Text("Motivo del Resultado")
    
    
    def _default_item_task(self):
        #return self.env['cam.item_task'].browse(self._context.get('active_ids')) # para varios registros.
        return self.env['cam.item_task'].browse(self._context.get('active_id'))

    item_task_id = fields.Many2one('cam.item_task', required=True, default=_default_item_task)

    def end(self):
        self.item_task_id.end(self)
        return {'type': 'ir.actions.act_window_close'}
