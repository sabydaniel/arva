from odoo import models, fields, api
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta


class SeaConsolWizard(models.TransientModel):
    _name = "sea.consol.wizard"
    _description = "Sea Export Consol Register Wizard"

    date_filter = fields.Selection([
        ("today", "Today"),
        ("yesterday", "Yesterday"),
        ("this_week", "This Week"),
        ("last_week", "Last Week"),
        ("this_month", "This Month"),
        ("last_month", "Last Month"),
        ("custom", "Custom"),
    ], default="this_month", string="Date Filter")

    date_from = fields.Date("Consol Date From", required=True)
    date_to = fields.Date("Consol Date To", required=True)

    branch_id = fields.Many2one("res.company", string="Branch")
    department_id = fields.Many2one("hr.department", string="Department")

    shipping_line_id = fields.Many2one("res.partner", string="Shipping Line")

    consol_type = fields.Selection([
        ("back_to_back", "Back To Back"),
        ("agent", "Agent's Consolidation")
    ], string="Consol Type")

    cargo_type = fields.Selection([
        ("fcl", "FCL"),
        ("lcl", "LCL")
    ], string="Cargo Type")

    port_of_load_id = fields.Many2one("res.country.state", string="Load Port")
    port_of_discharge_id = fields.Many2one("res.country.state", string="Disch. Port")

    status = fields.Selection([
        ("draft", "Draft"),
        ("confirmed", "Confirmed"),
        ("completed", "Completed"),
        ("cancel", "Cancelled")
    ], default="completed", string="Status")

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

    def generate_xlsx(self):
        domain = []

        if self.date_from:
            domain.append(("create_date", ">=", self.date_from))

        if self.date_to:
            domain.append(("create_date", "<=", self.date_to))

        if self.port_of_load_id:
            domain.append(("port_of_load_id", "=", self.port_of_load_id.id))

        if self.port_of_discharge_id:
            domain.append(("port_of_discharge_id", "=", self.port_of_discharge_id.id))

        if self.branch_id:
            domain.append(("branch_id", "=", self.branch_id.id))

        if self.department_id:
            domain.append(("department_id", "=", self.department_id.id))

        return {
            "type": "ir.actions.report",
            "report_type": "xlsx",
            "report_name": "shipping_report.simple_xlsx",
            "data": {
                "domain": domain,
                "date_from": self.date_from,
                "date_to": self.date_to,
                "branch": self.branch_id.name if self.branch_id else "",
            },
        }