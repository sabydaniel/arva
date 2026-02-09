{
    'name': 'Job Profit Charge Report',
    'version': '1.0',
    'depends': ['base', 'report_xlsx','shipping_proxy'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/jobprofit_by_charge_wizard_view.xml',
        'views/jobprofit_menu.xml',
    ],
    'installable': True,
}
