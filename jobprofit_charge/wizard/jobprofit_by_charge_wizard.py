from odoo import models, fields, api
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError


class JobProfitChargeReportWizard(models.TransientModel):
    _name = "job.profit.charge.report.wizard"
    _description = "Job Profit Charge Report Wizard"

    company_id = fields.Many2one(
        'res.company',
        string="Company",
        required=True,
        default=lambda self: self.env.company
    )

    branch_id = fields.Many2one(
        'res.company',
        string="Branch",
        domain="[('parent_id', '=', company_id)]"
    )

    date_filter = fields.Selection([
        ('today', 'Today'),
        ('this_month', 'This Month'),
        ('last_month', 'Last Month'),
        ('this_year', 'This Year'),
        ('custom', 'Custom Range')
    ], default='this_month')

    date_from = fields.Date(required=True)
    date_to = fields.Date(required=True)

    @api.onchange("date_filter")
    def _onchange_date_filter(self):
        today = date.today()

        if self.date_filter == 'today':
            self.date_from = self.date_to = today

        elif self.date_filter == 'this_month':
            self.date_from = today.replace(day=1)
            self.date_to = self.date_from + relativedelta(months=1, days=-1)

        elif self.date_filter == 'last_month':
            first = today.replace(day=1)
            last = first - timedelta(days=1)
            self.date_from = last.replace(day=1)
            self.date_to = last

        elif self.date_filter == 'this_year':
            self.date_from = today.replace(month=1, day=1)
            self.date_to = today.replace(month=12, day=31)

    @api.constrains('date_from', 'date_to')
    def _check_dates(self):
        for rec in self:
            if rec.date_from > rec.date_to:
                raise ValidationError("Date From must be before Date To.")

    def action_print_xlsx(self):
        self.ensure_one()

        data = {
            'company_id': self.company_id.id,
            'branch_id': self.branch_id.id,
            'date_from': self.date_from,
            'date_to': self.date_to,
        }

        return self.env.ref(
            'jobprofit_charge.action_jobprofit_by_charge_xlsx'
        ).report_action(self, data=data)
