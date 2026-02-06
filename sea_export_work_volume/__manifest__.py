{
    "name": "Sea Export Work Volume",
    "version": "1.0",
    "category": "Shipping",
    "summary": "Sea Export Work Volume Report",
    "depends": ["base", "web", "shipping_proxy","report_xlsx"],
    "data": [
        "security/ir.model.access.csv",
        "views/action.xml",
        "views/menu.xml",
        "views/wizard_view.xml",
        "report/work_volume_template.xml",
    ],
    "installable": True,
}
