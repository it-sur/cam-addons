# -*- coding: utf-8 -*-
{
    'name': "service",

    'summary': """
        CAM SRL, modulo de administracion de servicios""",

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
    'depends': ['base','hr','percent_field'],

    # always loaded
    'data': [
        'security/profiles_security.xml',
        'security/ir.model.access.csv',
        'views/mechanic.xml',
        'views/workshop.xml',
        'views/task.xml',
        'views/item_task_wizard.xml',
        'views/item_task.xml',
        'views/predefined_service.xml',
        'views/service.xml',
        'views/vehicle.xml',
        'views/menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
