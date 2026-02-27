from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta


class ShipmentStatusWizard(models.TransientModel):
    _name = "shipment.status.wizard"
    _description = "Sea Export Shipment Status Wizard"

    company_id = fields.Many2one(
        "res.company",
        string="Company",
        required=True,
        default=lambda self: self.env.company
    )

    branch_id = fields.Many2one(
        'res.company',
        string='Branch',
        required=True,
        domain="[('parent_id', '=', company_id)]"
    )

    department_id = fields.Many2one(
        "hr.department",
        string="Department"
    )

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)

        branch = self.env.user.branch_ids[:1]
        if branch:
            res['branch_id'] = branch.id

        return res

    @api.onchange("company_id")
    def _onchange_company(self):
        self.branch_id = False

    date_filter = fields.Selection(
        [
            ('today', 'Today'),
            ('yesterday', 'Yesterday'),
            ('this_week', 'This Week'),
            ('last_week', 'Last Week'),
            ('this_month', 'This Month'),
            ('last_month', 'Last Month'),
            ('this_year', 'This Year'),
            ('custom', 'Custom Range'),
        ],
        string="Date Range",
        default='this_month'
    )

    date_from = fields.Date(
        string="Shipment Date From",
        default=lambda self: fields.Date.today().replace(day=1)
    )

    date_to = fields.Date(
        string="Shipment Date To",
        default=fields.Date.today
    )

    shipper_id = fields.Many2one(
        "res.partner",
        string="Shipper"
    )

    consignee_id = fields.Many2one(
        "res.partner",
        string="Consignee"
    )

    @api.onchange("date_filter")
    def _onchange_date_filter(self):
        today = date.today()

        if self.date_filter == "today":
            self.date_from = today
            self.date_to = today

        elif self.date_filter == "yesterday":
            y = today - timedelta(days=1)
            self.date_from = y
            self.date_to = y

        elif self.date_filter == "this_week":
            start = today - timedelta(days=today.weekday())
            self.date_from = start
            self.date_to = start + timedelta(days=6)

        elif self.date_filter == "last_week":
            start = today - timedelta(days=today.weekday() + 7)
            self.date_from = start
            self.date_to = start + timedelta(days=6)

        elif self.date_filter == "this_month":
            start = today.replace(day=1)
            self.date_from = start
            self.date_to = start + relativedelta(months=1, days=-1)

        elif self.date_filter == "last_month":
            last_day = today.replace(day=1) - timedelta(days=1)
            self.date_from = last_day.replace(day=1)
            self.date_to = last_day

        elif self.date_filter == "this_year":
            self.date_from = today.replace(month=1, day=1)
            self.date_to = today.replace(month=12, day=31)

    @api.constrains("date_from", "date_to")
    def _check_date(self):
        for rec in self:
            if rec.date_from and rec.date_to and rec.date_from > rec.date_to:
                raise ValidationError("From Date cannot be after To Date")

    def action_generate_xlsx(self):
        self.ensure_one()

        domain = []

        if self.date_from:
            domain.append(('hbl_date', '>=', self.date_from))

        if self.date_to:
            domain.append(('hbl_date', '<=', self.date_to))

        if self.branch_id:
            domain.append(('branch_id', '=', self.branch_id.id))

        if self.shipper_id:
            domain.append(('hbl_consigner_id', '=', self.shipper_id.id))

        if self.consignee_id:
            domain.append(('hbl_consignee_id', '=', self.consignee_id.id))

        return {
            "type": "ir.actions.report",
            "report_type": "xlsx",
            "report_name": "shipping_report.shipment_status_xlsx",
            "data": {
                "domain": domain,
                "date_from": self.date_from,
                "date_to": self.date_to,
                "branch_name": self.branch_id.name if self.branch_id else "",
            },
        }
