from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta


class UnbilledJobsWizard(models.TransientModel):
    _name = 'unbilled.jobs.wizard'
    _description = 'Unbilled Jobs Wizard'

    date_filter = fields.Selection([
        ("today", "Today"),
        ("yesterday", "Yesterday"),
        ("this_week", "This Week"),
        ("last_week", "Last Week"),
        ("this_month", "This Month"),
        ("last_month", "Last Month"),
        ("custom", "Custom"),
    ], default="this_month", string="Date Filter")

    date_from = fields.Date("From Date")
    date_to = fields.Date("To Date")

    branch_id = fields.Many2one(
        "res.company",
        string="Branch",
        default=lambda self: self.env.company
    )

    invoiced = fields.Boolean(string='Invoiced', default=False)
    purchased = fields.Boolean(string='Purchased', default=False)

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
            first_day_last_month = today.replace(day=1) - relativedelta(months=1)
            last_day_last_month = first_day_last_month + relativedelta(day=31)
            self.date_from = first_day_last_month
            self.date_to = last_day_last_month

        elif self.date_filter == "custom":
            self.date_from = False
            self.date_to = False

    def action_generate_report(self):

        domain = []

        if self.branch_id:
            domain.append(('branch_id', '=', self.branch_id.id))

        if self.date_from:
            domain.append(('hbl_date', '>=', self.date_from))

        if self.date_to:
            domain.append(('hbl_date', '<=', self.date_to))

        if self.invoiced and not self.purchased:
            domain.append(('invoice_count', '>', 0))

        elif self.purchased and not self.invoiced:
            domain.append(('purchase_count', '>', 0))

        elif self.invoiced and self.purchased:
            domain += [
                '|',
                ('invoice_count', '>', 0),
                ('purchase_count', '>', 0)
            ]

        shipments = self.env['ship.shipment'].search(domain)

        if not shipments:
            raise UserError("No records found for selected filters.")

        return self.env.ref(
            'shipping_report.unbilled_jobs_xlsx'
        ).report_action(shipments)