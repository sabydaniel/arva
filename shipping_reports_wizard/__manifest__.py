{
    'name': 'Shipping Reports Wizard',
    'version': '1.0',
    'summary': 'Shipment PDF auto attach, preview and send',
    'category': 'Shipping',
    'depends': ['base','mail','web','shipping_proxy',],
    'data': [
        'security/ir.model.access.csv',
        'report/shipment_report.xml',
        'report/shipment_report_template.xml',
        'data/shipment_mail_template.xml',
        'views/shipment_report_wizard_view.xml',
        'views/shipment_report_menu.xml',
    ],
    'installable': True,
}
