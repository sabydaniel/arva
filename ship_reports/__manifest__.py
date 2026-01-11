{
    'name': 'Ship Reports',
    'version': '1.0',
    'summary': 'Shipping reports with PDF and XLSX export',
    'depends': ['base','web','report_xlsx',],
    'data': [
        'security/ir.model.access.csv',
        'views/ship_reports_actions.xml',
        'views/ship_reports_menu.xml',
        'views/ship_reports_list_view.xml',
        'views/ship_reports_wizard_view.xml',
        'report/ship_report_pdf.xml',
        'report/ship_report_qweb.xml',
        'report/ship_report_qweb_template.xml',
        'report/ship_report_xlsx.xml',
    ],
    'installable': True,
    'application': True,
}
