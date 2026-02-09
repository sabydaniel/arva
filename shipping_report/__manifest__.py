{
    'name': 'Shipping Report',
    'version': '17.0.1.0.0',
    'summary': 'Centralized Shipping Reports Module',
    'description': """
        Shipping Reporting Module
        Includes:
        - Job Profit By Charge
        - Sea Export Consol Register
        - Shipment Report
        - Work Volume Report
        - Future reports""",
    'category': 'Reporting',
    'author': 'Your Company',
    'depends': ['base','web','report_xlsx','shipping_proxy',],
    'data': [
        'security/ir.model.access.csv',
        'wizard/jobprofit_by_charge_wizard_view.xml',
        'wizard/sea_consol_wizard_view.xml',
        'wizard/ship_report_wizard.xml',
        'wizard/work_volume_wizard_view.xml',
        'report/sea_consol_report_xlsx.xml',
        'report/ship_report_qweb.xml',
        'report/ship_report_xlsx.xml',
        'report/work_volume_template.xml',
        'views/jobprofit_menu.xml',
        'views/sea_consol_menu.xml',
        'views/sea_export_action.xml',
        'views/sea_export_menu.xml',
        'views/ship_report_actions.xml',
        'views/ship_report_menu.xml',
    ],
    'installable': True,
    'application': True,
}
