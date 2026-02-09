from odoo import models, fields, api
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta


class ShipQuoteVsTransactionWizard(models.TransientModel):
    _name = "ship.quote.transaction.wizard"
    _description = "Quotation Vs Transaction Wizard"

    department_id = fields.Many2one(
        "hr.department",
        string="Department"
    )

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
        string="Quotation Date From",
        required=True,
        default=lambda self: fields.Date.today().replace(day=1)
    )

    date_to = fields.Date(
        string="Quotation Date To",
        required=True,
        default=fields.Date.today
    )

    status = fields.Selection(
        [
            ("draft", "Draft"),
            ("valid", "Valid"),
            ("expired", "Expired"),
            ("converted", "Converted"),
        ],
        string="Status"
    )

    quoted_to_id = fields.Many2one(
        "res.partner",
        string="Quoted To"
    )

    quoted_by_id = fields.Many2one(
        "res.users",
        string="Quoted By"
    )

    branch_id = fields.Many2one(
        "res.company",
        string="Branch",
        default=lambda self: self.env.user.branch_ids[:1]
    )


    @api.onchange('date_filter')
    def _onchange_date_filter(self):
        today = fields.Date.today()

        if self.date_filter == 'today':
            self.date_from = today
            self.date_to = today

        elif self.date_filter == 'yesterday':
            day = today - timedelta(days=1)
            self.date_from = day
            self.date_to = day

        elif self.date_filter == 'this_week':
            start = today - timedelta(days=today.weekday())
            self.date_from = start
            self.date_to = start + timedelta(days=6)

        elif self.date_filter == 'last_week':
            end = today - timedelta(days=today.weekday() + 1)
            self.date_to = end
            self.date_from = end - timedelta(days=6)

        elif self.date_filter == 'this_month':
            start = today.replace(day=1)
            self.date_from = start
            self.date_to = (start + relativedelta(months=1)) - timedelta(days=1)

        elif self.date_filter == 'last_month':
            start = today.replace(day=1) - relativedelta(months=1)
            self.date_from = start
            self.date_to = today.replace(day=1) - timedelta(days=1)

        elif self.date_filter == 'this_year':
            self.date_from = date(today.year, 1, 1)
            self.date_to = date(today.year, 12, 31)


    def action_export_xlsx(self):
        self.ensure_one()
        return self.env.ref(
            "ship_quote_vs_transaction.action_ship_quote_vs_transaction_xlsx"
        ).report_action(self)
