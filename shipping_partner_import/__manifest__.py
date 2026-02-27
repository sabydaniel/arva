{
    'name': 'Shipping Organization Import',
    'version': '17.0.1.0.0',
    'depends': [
        'base',
        'shipping_proxy',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/organization_view.xml',
        'views/organization_import_wizard_view.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': True,
}
