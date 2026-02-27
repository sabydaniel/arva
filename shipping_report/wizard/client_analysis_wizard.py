from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import timedelta
from dateutil.relativedelta import relativedelta


class ClientAnalysisWizard(models.TransientModel):
    _name = "client.analysis.wizard"
    _description = "Client Analysis Wizard"

    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
        default=lambda self: self.env.company
    )

    branch_id = fields.Many2one(
        'res.company',
        string='Branch',
        required=True,
        domain="[('parent_id', '=', company_id)]"
    )

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)

        # Default branch from user
        branch = self.env.user.branch_ids[:1]
        if branch:
            res['branch_id'] = branch.id

        return res

    @api.onchange('company_id')
    def _onchange_company(self):
        self.branch_id = False

    report_by = fields.Selection(
        [("billing", "Billing Client")],
        string="Report By",
        default="billing",
        required=True
    )

    analyse_by = fields.Selection(
        [("local_job", "Analyse by Local Client on Job")],
        string="Analyse By",
        default="local_job",
        required=True
    )

    billing_client_id = fields.Many2one(
        "res.partner",
        string="Billing Client",
        domain=[("is_company", "=", True)]
    )

    local_client_id = fields.Many2one(
        "res.partner",
        string="Local Client",
        domain=[("is_company", "=", True)]
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
        default='this_month',
        required=True
    )

    period1_from = fields.Date(
        string="Period 1 From",
        required=True,
        default=lambda self: fields.Date.context_today(self).replace(day=1)
    )

    period1_to = fields.Date(
        string="Period 1 To",
        required=True,
        default=lambda self: fields.Date.context_today(self)
    )

    date_filter_p2 = fields.Selection(
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
        default='custom'
    )

    period2_from = fields.Date(string="Period 2 From")
    period2_to = fields.Date(string="Period 2 To")

    @api.onchange('date_filter')
    def _onchange_date_filter(self):
        today = fields.Date.context_today(self)

        if self.date_filter == 'today':
            self.period1_from = today
            self.period1_to = today

        elif self.date_filter == 'yesterday':
            d = today - timedelta(days=1)
            self.period1_from = d
            self.period1_to = d

        elif self.date_filter == 'this_week':
            start = today - timedelta(days=today.weekday())
            self.period1_from = start
            self.period1_to = start + timedelta(days=6)

        elif self.date_filter == 'last_week':
            start = today - timedelta(days=today.weekday() + 7)
            self.period1_from = start
            self.period1_to = start + timedelta(days=6)

        elif self.date_filter == 'this_month':
            start = today.replace(day=1)
            self.period1_from = start
            self.period1_to = start + relativedelta(months=1) - timedelta(days=1)

        elif self.date_filter == 'last_month':
            start = today.replace(day=1) - relativedelta(months=1)
            self.period1_from = start
            self.period1_to = today.replace(day=1) - timedelta(days=1)

        elif self.date_filter == 'this_year':
            self.period1_from = today.replace(month=1, day=1)
            self.period1_to = today.replace(month=12, day=31)

    @api.onchange('date_filter_p2')
    def _onchange_date_filter_p2(self):
        today = fields.Date.context_today(self)

        if self.date_filter_p2 == 'today':
            self.period2_from = today
            self.period2_to = today

        elif self.date_filter_p2 == 'yesterday':
            d = today - timedelta(days=1)
            self.period2_from = d
            self.period2_to = d

        elif self.date_filter_p2 == 'this_week':
            start = today - timedelta(days=today.weekday())
            self.period2_from = start
            self.period2_to = start + timedelta(days=6)

        elif self.date_filter_p2 == 'last_week':
            start = today - timedelta(days=today.weekday() + 7)
            self.period2_from = start
            self.period2_to = start + timedelta(days=6)

        elif self.date_filter_p2 == 'this_month':
            start = today.replace(day=1)
            self.period2_from = start
            self.period2_to = start + relativedelta(months=1) - timedelta(days=1)

        elif self.date_filter_p2 == 'last_month':
            start = today.replace(day=1) - relativedelta(months=1)
            self.period2_from = start
            self.period2_to = today.replace(day=1) - timedelta(days=1)

        elif self.date_filter_p2 == 'this_year':
            self.period2_from = today.replace(month=1, day=1)
            self.period2_to = today.replace(month=12, day=31)

    @api.constrains('period1_from', 'period1_to', 'period2_from', 'period2_to')
    def _check_dates(self):
        for rec in self:
            if rec.period1_from and rec.period1_to and rec.period1_from > rec.period1_to:
                raise ValidationError("Period 1 From must be before Period 1 To")

            if rec.period2_from and rec.period2_to and rec.period2_from > rec.period2_to:
                raise ValidationError("Period 2 From must be before Period 2 To")

    def action_export_xlsx(self):
        self.ensure_one()

        return self.env.ref(
            "shipping_report.shipping_report_client_analysis_xlsx"
        ).report_action(self, data={
            "branch_id": self.branch_id.id,
            "billing_client_id": self.billing_client_id.id if self.billing_client_id else False,
            "local_client_id": self.local_client_id.id if self.local_client_id else False,
            "period1_from": self.period1_from,
            "period1_to": self.period1_to,
            "period2_from": self.period2_from,
            "period2_to": self.period2_to,
        })