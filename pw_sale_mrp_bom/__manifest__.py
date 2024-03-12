# -*- coding: utf-8 -*-
{
    'name': 'Manufacturing Bom in Sale Order Line',
    'version': '1.0',
    'author': "Adham Mohamed",
    'category': 'Sales',
    'depends': ['sale_mrp'],
    'summary': 'This app helps you to select manufacturing bill of material in sale order line | Manufacturing Bom in Sale Order Line | BoM selection on sale order line | Select bom from sale line',
    'description': """This app helps you to select manufacturing bill of material in sale order line""",
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_view.xml',
        'views/bom.xml',
        'data/data.xml',
    ],
    "license": "LGPL-3",
    'installable': True,
}
