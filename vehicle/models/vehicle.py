# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class vehicle(models.Model):
    _name = 'cam.vehicle'
    _description = 'cam.vehicle'
    _inherit = ["cam.maintainable_object"]

    nro_interno = fields.Char("Nro interno")

    patent = fields.Char(string="Patente", track_visibility='onchange')

    sector_id = fields.Many2one('cam.sector',string="Sector")
    
    function_id = fields.Many2one('cam.function',string="Funcion")



    @api.onchange('sector_id')
    def onchange_sector_id(self):
        res = {
            'domain' : {
                'function_id' : [('id', 'in', [x.id for x in self.sector_id.function_ids])],
            }
        }
        self.function_id = False
        return res


    engine_id = fields.Many2one("cam.engine",string="Motor")


    model_id = fields.Many2one("cam.vehicle_model", string="Modelo", track_visibility='onchange')
    brand_id = fields.Many2one(related="model_id.brand_id", string="Marca")


    out_of_service_reason_ids = fields.One2many(comodel_name='cam.out_of_service_reason_vehicle',inverse_name="vehicle_id",
                                                 string='Razones de fuera de servicio')

    
    
    fabricante_origen_anio = fields.Char(string="Fabricante/Origen/Año", readonly=True, 
                                         compute="_compute_vin", help='Datos segun nro de chasis')
    nro_chasis = fields.Char(string="Nro de Chasis", track_visibility='onchange')
    serie_vin = fields.Char(string="Serie/Vin", readonly=True, compute="_compute_vin")

    
    
    anio = fields.Selection([('2014', '2014'),
                             ('2015', '2015'),
                             ('2016', '2016'),
                             ('2017', '2017'),
                             ('2018', '2018'),
                             ('2019', '2019'),
                             ('2020', '2020'),
                             ('2021', '2021'),
                             ('2022', '2022'),
                             ('2023', '2023'),
                             ('2024', '2024'),
                             ('2025', '2025'),
                             ('2026', '2026')],
                             'Modelo Año', copy=False, default='2018')
    
    
    anios = {
              'A':'2009',
              'B':'2010',
              'C':'2011',
              'D':'2012',
              'E':'2013',
              'F':'2014',
              'G':'2015',
              'H':'2016',
              'I':'2017',
              'J':'2018',
              'K':'2019',
              'L':'2020',
              'M':'2021',
              'N':'2022',
              'P':'2023',
              'R':'2024',
              'S':'2025',
              'T':'2026',
              'V':'2027',
              'W':'2028',
              'X':'2029',
              'Y':'2030',
              '1':'2031',
              '2':'2032',
              '3':'2033',
              '4':'2034',
              '5':'2035',
              '6':'2036',
              '7':'2037',
              '8':'2038',
              '9':'2039',
              }
    
    origenes = {'1':'EEUU',
               '4':'EEUU',
               '5':'EEUU',
               '2':'Canada',
               '3':'Mexico',
               'A':'Sudafrica',
               'J':'Japon',
               'K':'Corea del Sur',
               'L':'China',
               'M':'India-Indonesia-Tailandia',
               'P':'Filipinas-Malasia',
               'S':'Reino Unido-Alemania-Polonia',
               'T':'Suiza-Rep.Checa-Ungria',
               'V':'Austria-Francia-España',
               'X':'Rusia',
               'W':'Alemania',
               'Y':'Belgica-Finlandia-Suecia',
               'Z':'Italia',
               '6':'Australia',
               '7':'Nueva Zelanda',
               '8':'Arg-Chi-Ven',
               '9':'Bra-Col',
               }

    fabricantes = {
              'A':'Audi-Jaguar',
              'B':'BMW-Dodge',
              'F':'Ford-Renault-Citroen',
              'C':'Chevrolet-Chrysler',
              '7':'GM',
              'G':'GM',
              'n':'Honda',
              'D':'Mercedes',
              'N':'Nissan',
              'S':'Saab',
              'T':'Toyota',
              'V':'Volkswagen',
             }

    modelos = {
               '6P8CF':'Mustang',
               'ZH55K':'Ka',
               'ZH54K':'Ka',
               'Z55A9':'Ka',
               'ZH55K':'Ka',
               
               'BZZFH':'Focus',
               'BZZFF':'Focus',
               'NZZFH':'Focus',

               'ZD55N':'Fiesta',
               'FP4WJ':'Fiesta',
               'DP4YJ':'Fiesta',
               'DP4ZJ':'Fiesta',

               'ZB55N':'Ecosport',
               'ZB55U':'Ecosport',

               'AR22K':'Ranger',
               'AR22W':'Ranger',

               '6P0H9':'Mondeo',

               'ADAWP':'Kuga',

               'YEA8E':'Cargo',
               'YEAHD':'Cargo',
               'YEAKD':'Cargo',
               'YEAXV':'Cargo',
               'YEB2B':'Cargo',
               'YEB2B':'Cargo',
               'YEB5J':'Cargo',
               'VEADS':'Cargo',

               'LF49P':'4000',
                       
               }
        
    @api.constrains('patent')
    def check_patente(self):
        for record in self:
            pat = record.patent
            if not bool(pat): return
            anio = record.anio
            if not bool(anio): return
            if ((len(pat) != 6) and (len(pat) != 7)):
                raise ValidationError("El campo patente debe tener 6 o 7 caracteres.")
                return
            elif (len(pat) == 6) & (int(anio) < 2017) :
                if not pat[3:6].isdigit():
                    raise ValidationError("El campo patente no posee los 3 numeros.")
                    return
                if not pat[0:3].isalpha():
                    raise ValidationError("El campo patente no posee las 3 letras.")
                    return    
            elif (len(pat) == 7) & (int(anio) >= 2016):
                if not pat[0:2].isalpha():
                    raise ValidationError("Los primeros dos dígitos de la patente deben ser letras")
                    return
                if not pat[2:5].isdigit():
                    raise ValidationError("Los digitos 3 4 y 5 de la patente deben ser números")
                    return
                if not pat[5:7].isalpha():
                    raise ValidationError("Los últimos dos dígitos de la patente deben ser letras")
                    return
            # Se quita la obligacion de cargar patente.
            # Revisar en que momento hay que obligar cargarla.
            else: 
                raise ValidationError("La patente es invalida")
                return
                
    @api.onchange('patent')
    def onchange_patent(self):
        for rec in self:
            if rec.patent:
                rec.patent = str(rec.patent).upper()



            
    @api.onchange('nro_chasis')
    def upper_chasis(self):
        if self.nro_chasis:
            self.nro_chasis = str(self.nro_chasis).upper()
        
    _sql_constraints = [
            ('vehicle_chasis_unique', 'unique(nro_chasis)', 'El chasis ya existe'),
            ('vehicle_nro_interno', 'unique(nro_interno)', 'El nro de interno ya existe'),
            ('vehicle_patent', 'unique(patent)', 'La patente ya existe'),
    ]

    @api.constrains('nro_chasis')
    def check_chasis(self):
        vehicles = self.env['cam.vehicle'].search([('nro_chasis', 'ilike', self.nro_chasis)])
        if len(vehicles) > 1:
            raise ValidationError("El nro de chasis ya existe.")
            return False

        ## limit validation
        return
        
        if not (len(self.nro_chasis) == 17):
            raise ValidationError("El nro de chasis debe tener 17 digitos.")
            return False
        
        valid_chasis = True
        
        if not (self.nro_chasis[:1] in self.origenes):
            valid_chasis = False
        if 'W' == self.nro_chasis[:1]:
            if not (self.nro_chasis[1:2] in self.fabricantes):
                valid_chasis = False
        else:
            if not (self.nro_chasis[9:10] in self.anios):
                valid_chasis = False
            if not (self.nro_chasis[2:3] in self.fabricantes):
                valid_chasis = False
    
        if (not valid_chasis):
            raise ValidationError("El nro de chasis es invalido.")
            return False



    @api.depends('nro_chasis')
    def _compute_vin(self):
        origen = 'Desconocido'
        anio = 'Desconocido'
        fabricante = 'Desconocida'
        modelo = ''
        for rec in self:
            if bool(rec.nro_chasis):
                rec.serie_vin = rec.nro_chasis[-8:]
    
    
                if (len(rec.nro_chasis) == 17):
                    if rec.nro_chasis[:1] in rec.origenes:
                        origen = rec.origenes[rec.nro_chasis[:1]]
                    if 'W' == rec.nro_chasis[:1]:
                        if rec.nro_chasis[1:2] in rec.fabricantes:
                            fabricante = rec.fabricantes[rec.nro_chasis[1:2]]
                    else:
                        if rec.nro_chasis[2:3] in rec.fabricantes:
                            fabricante = rec.fabricantes[rec.nro_chasis[2:3]]
                        if rec.nro_chasis[9:10] in rec.anios:
                            anio = rec.anios[rec.nro_chasis[9:10]]
    
                    if rec.nro_chasis[3:8] in rec.modelos:
                        modelo = '/' + rec.modelos[rec.nro_chasis[3:8]]
    
            rec.fabricante_origen_anio = str(fabricante) + '/' + str(origen) + '/' + str(anio) + str(modelo)
        




#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
