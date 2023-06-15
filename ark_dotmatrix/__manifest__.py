# -*- coding: utf-8 -*-
{
    'name': "Dotmatrix",

    'summary': """
        This addon for integrate to dotmatrix printer""",

    'description': """
    """,

    'author': "Faris Maulana Kholifiar",
    'website': "www.linkedin.com/in/farismaulana",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','ark_sale','stock','partner_fax','ark_account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/web_asset.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'ark_dotmatrix/static/src/js/print_button.js',
        ],
    },
}
