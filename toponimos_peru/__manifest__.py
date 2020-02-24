# -*- coding: utf-8 -*-
{
    'name': "Toponimos de Peru",

    'summary': """
        Ubigeo Departamentos, Provincias y distritos del Peru según INEI.""",

    'description': """
Localizacion Peruana.
====================================

Clientes y Proveedores:
--------------------------------------------
    * Tabla de Ubigeos - Según INEI 2016
    * Departamentos, provincias y distritos de todo el Perú

    """,

    'author': "",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/res_partner_view.xml',
        'views/res_country_view.xml',
        'data/res.country.state.csv',
        'data/patch1/res.country.state.csv',
        'data/patch2/res.country.state.csv',
    ],
    # only loaded in demonstration mode
    'demo': [],
}
