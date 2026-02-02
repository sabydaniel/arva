{
    'name': 'Ship Report',
    'version': '17.0.1.0.0',
    'category': 'Shipping',
    'summary': 'Shipping Job Reports',
    'depends': ['base', 'web', 'report_xlsx', 'shipping_proxy'],
    "data": [
        "security/ir.model.access.csv",
        "views/ship_report_menu.xml",
        "wizard/ship_report_wizard.xml",
        "views/ship_report_actions.xml",
        "report/ship_report_qweb.xml",
        "report/ship_report_xlsx.xml",
    ],

    'installable': True,
    "application": True,
}
