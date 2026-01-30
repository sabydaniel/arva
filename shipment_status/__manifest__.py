{
    "name": "Shipment Status Register",
    "version": "17.0.1.0.0",
    "category": "Shipping",
    "summary": "Sea Export Shipment Status Register",
    "depends": [
        "base",
        "web",
        "shipping_proxy",
        "report_xlsx",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/shipment_status_wizard_view.xml",
        "views/menu.xml",
        "report/shipment_status_report.xml",
    ],
    "installable": True,
}
