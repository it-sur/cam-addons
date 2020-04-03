# -*- coding: utf-8 -*-
{
    'name': "vehicle",

    'summary': """
        CAM SRL, modulo de administracion de vehiculos""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Route IT",
    'website': "http://www.routeit.com.ar",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'CAM SRL',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','cam_base'],

    # always loaded
    'data': [
        'security/profiles_security.xml',
        'security/ir.model.access.csv',
        'views/brand.xml',
        'views/engine.xml',
        'views/tool_model.xml',
        'views/tool.xml',
        'views/vehicle_model.xml',
        'views/vehicle.xml',
        'views/menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
