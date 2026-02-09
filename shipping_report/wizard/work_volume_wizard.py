from odoo import models, fields, api
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta


class SeaExportWorkVolumeWizard(models.TransientModel):
    _name = "sea.export.work.volume.wizard"
    _description = "Sea Export Work Volume Wizard"

    date_filter = fields.Selection([
        ("today", "Today"),
        ("yesterday", "Yesterday"),
        ("this_week", "This Week"),
        ("last_week", "Last Week"),
        ("this_month", "This Month"),
        ("last_month", "Last Month"),
        ("custom", "Custom"),
    ], default="this_month", string="Date Filter")

    date_from = fields.Date("From Date", required=True)
    date_to = fields.Date("To Date", required=True)

    type = fields.Selection([
        ("summary", "Summary"),
    ], default="summary", string="Type")

    branch_id = fields.Many2one("res.company", string="Branch")

    shipper_id = fields.Many2one("res.partner", "Shipper")
    consignee_id = fields.Many2one("res.partner", "Consignee")
    shipping_line_id = fields.Many2one("res.partner", "Shipping Line")

    consol_type = fields.Selection([
        ("all", "All"),
        ("back_to_back", "Back To Back"),
        ("agent", "Agent"),
    ], default="all", string="Consol Type")

    cargo_type = fields.Selection([
        ("all", "All"),
        ("fcl", "FCL"),
        ("lcl", "LCL"),
    ], default="all", string="Cargo Type")

    load_port_id = fields.Many2one("res.country.state", string="Load Port")
    discharge_port_id = fields.Many2one("res.country.state", string="Discharge Port")

    @api.onchange("date_filter")
    def _onchange_date_filter(self):
        today = date.today()

        if self.date_filter == "today":
            self.date_from = today
            self.date_to = today

        elif self.date_filter == "yesterday":
            d = today - timedelta(days=1)
            self.date_from = d
            self.date_to = d

        elif self.date_filter == "this_week":
            start = today - timedelta(days=today.weekday())
            self.date_from = start
            self.date_to = start + timedelta(days=6)

        elif self.date_filter == "last_week":
            start = today - timedelta(days=today.weekday() + 7)
            self.date_from = start
            self.date_to = start + timedelta(days=6)

        elif self.date_filter == "this_month":
            self.date_from = today.replace(day=1)
            self.date_to = today

        elif self.date_filter == "last_month":
            first = today.replace(day=1) - relativedelta(months=1)
            self.date_from = first
            self.date_to = first + relativedelta(day=31)
    def action_generate_pdf(self):
        return self.env.ref(
            "shipping_report.action_report_sea_export_work_volume"
        ).report_action(self)
