# -*- coding: utf-8 -*-
{
    'name': "Cuba - Configuración base",

    'summary': """
        Configuración base para Cuba""",

    'description': """
        Configuración para Cuba: organismos, provincias, municipios, etc.
    """,
    'author': "MSc. Alexander Vinent Peña[alexander.vinent@scu.desoft.cu]",
    'website': "http://www.twitter.com/alecko",
    'category': 'Localization',
    'version': '10.0.1.2',
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/
        'security/ir.model.access.csv',

        'data/provincias_municipios_data.xml',
        'data/res_partner_organismo_data.xml',
        'data/res_partner_tipo_data.xml',
        'data/res_partner_subordinacion_data.xml',
        'data/res_currency_data.xml',
        'data/res_partner_data.xml',
        'data/cron.xml',

        'views/res_country_state_municipio_view.xml',
        'views/res_partner_view.xml',

        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [],
    'active': False,
    'installable': True
}
