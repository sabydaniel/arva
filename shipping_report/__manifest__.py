{
    "name": "Shipping Reports",
    "version": "17.0.1.0.0",
    "category": "Reporting",
    "summary": "All Shipping Reports in One Module",
    "depends": [
        "base",
        "shipping_proxy",
        "report_xlsx",
    ],
    "data": [

        "security/ir.model.access.csv",

        "views/report_actions.xml",

        "report/shipment_status_report.xml",


        "wizard/shipment_revenue_wizard_view.xml",
        "report/shipment_revenue_xlsx.xml",


        "wizard/ship_quote_vs_transaction_wizard_view.xml",
        "report/ship_quote_transaction_xlsx.xml",


        "wizard/client_analysis_wizard_view.xml",
        "report/client_analysis_xlsx.xml",


        "wizard/job_count_summary_wizard_view.xml",
        "report/job_count_summary_xlsx.xml",
        "report/job_count_summary_template.xml",


        "views/menu.xml",
    ],
    "installable": True,
    "application": False,
}
