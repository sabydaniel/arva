{
    'name': 'Shipment Import',
    'version': '17.0.1.0.0',
    'depends': ['base', 'shipping_proxy'],
    'data': [
        'security/ir.model.access.csv',
        'views/shipment_views.xml',
        'wizard/shipment_import_wizard_view.xml',
        'views/shipment_import_menu.xml',
    ],

    'installable': True,
    'application': True,
}
