# -*- coding: utf-8 -*-

from odoo import models, fields, api


class engine(models.Model):
    _name = 'cam.engine'
    _description = 'cam.engine'

    name = fields.Char("Nombre")
    description = fields.Char("Descripcion")
    transmission = fields.Char("Transmision")


    consumption = fields.Integer("Consumo estandard")
    consumption_measure = fields.Selection([("kml", "KM/L"),
                                                 ("mil","Mi/L"),
                                                 ("l100km","L/100km"),
                                                 ("lh","L/Hora"),
                                                 ("kwatt","Kilo Watt/Hora"),
                                                 ],string="Medida del consumo")
    
    fuel_type  = fields.Selection([
                                          ("bio-diesel","Biodiesel"),
                                          ("diesel","diesel"),
                                          ("nafta","Nafta"),
                                          ("e_220v","220V"),
                                          ("hibrid","Hibrido"),
                                          ("gas","Gas"),
                                          ("otro","otro"),
                                          ],"Tipo de combustible")

    
    
    cilinder = fields.Char("Cilindrada")
    horsepower  = fields.Char("Caballos de fuerza")
    co2  = fields.Char("Emisiones")

    powerkw = fields.Char("Potencia")
    
    odometer = fields.Integer("Odometro/Horometro")
    odometer_unit = fields.Selection([("hours","Horometro"),
                                          ("odo_km","Kilometro"),
                                          ("odo_mi","Millas"),
                                          ],"Unidad")

    
    
    
