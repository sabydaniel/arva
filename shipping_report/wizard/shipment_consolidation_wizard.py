from odoo import models, fields, api
from datetime import date
from dateutil.relativedelta import relativedelta


class ShipmentConsolidationWizard(models.TransientModel):
    _name = "shipment.consolidation.wizard"
    _description = "Shipment Consolidation Wizard"
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
        default=lambda self: self.env.company
    )

    branch_id = fields.Many2one(
        'res.company',
        string='Branch',
        domain="[('parent_id', '=', company_id)]"
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
        default='this_month',
        string="Date Range"
    )

    date_from = fields.Date(
        string="Shipment Date From",
        default=lambda self: fields.Date.today().replace(day=1)
    )

    date_to = fields.Date(
        string="Shipment Date To",
        default=fields.Date.today
    )

    shipper_id = fields.Many2one("res.partner", string="Shipper")
    consignee_id = fields.Many2one("res.partner", string="Consignee")

    joborder_id = fields.Many2one(
        "ship.joborder",
        string="Job Order"
    )



    @api.onchange("date_filter")
    def _onchange_date_filter(self):
        today = date.today()

        if self.date_filter == "today":
            self.date_from = today
            self.date_to = today

        elif self.date_filter == "yesterday":
            d = today - relativedelta(days=1)
            self.date_from = d
            self.date_to = d

        elif self.date_filter == "this_week":
            start = today - relativedelta(days=today.weekday())
            self.date_from = start
            self.date_to = start + relativedelta(days=6)

        elif self.date_filter == "last_week":
            start = today - relativedelta(days=today.weekday() + 7)
            self.date_from = start
            self.date_to = start + relativedelta(days=6)

        elif self.date_filter == "this_month":
            self.date_from = today.replace(day=1)
            self.date_to = today

        elif self.date_filter == "last_month":
            first_day = today.replace(day=1) - relativedelta(months=1)
            last_day = today.replace(day=1) - relativedelta(days=1)
            self.date_from = first_day
            self.date_to = last_day

        elif self.date_filter == "this_year":
            self.date_from = today.replace(month=1, day=1)
            self.date_to = today



    def action_generate(self):
        self.ensure_one()

        domain = [('state', '!=', 'cancel')]

        if self.date_from:
            domain.append(('hbl_date', '>=', self.date_from))

        if self.date_to:
            domain.append(('hbl_date', '<=', self.date_to))

        if self.shipper_id:
            domain.append(('hbl_consigner_id', '=', self.shipper_id.id))

        if self.consignee_id:
            domain.append(('hbl_consignee_id', '=', self.consignee_id.id))

        if self.branch_id:
            domain.append(('branch_id', '=', self.branch_id.id))

        if self.joborder_id:
            domain.append(('joborder_id', '=', self.joborder_id.id))

        data = {
            'domain': domain,
            'date_from': self.date_from,
            'date_to': self.date_to,
            'branch_name': self.branch_id.name if self.branch_id else '',
        }

        return self.env.ref(
            'shipping_report.shipping_report_shipment_consolidation_xlsx'
        ).report_action(self, data=data)
