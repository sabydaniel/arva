from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta


class ShipmentRevenueWizard(models.TransientModel):
    _name = 'shipment.revenue.wizard'
    _description = 'Sea Export Shipment Register - Revenue'

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

    @api.onchange('company_id')
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
        default='this_month',
        string="Date Range"
    )

    date_from = fields.Date(
        string='From Date',
        required=True,
        default=lambda self: fields.Date.today().replace(day=1)
    )

    date_to = fields.Date(
        string='To Date',
        required=True,
        default=fields.Date.today
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

    shipper_id = fields.Many2one('res.partner', string='Shipper')
    consignee_id = fields.Many2one('res.partner', string='Consignee')
    shipping_line_id = fields.Many2one('res.partner', string='Shipping Line')
    destination_agent_id = fields.Many2one('res.partner', string='Destination Agent')

    load_port_id = fields.Many2one('ship.port', string='Load Port')
    discharge_port_id = fields.Many2one('ship.port', string='Discharge Port')

    consol_type = fields.Selection(
        [('fcl', 'FCL'), ('lcl', 'LCL'), ('breakbulk', 'Break Bulk')],
        string='Consol Type'
    )

    cargo_type = fields.Selection(
        [
            ('general', 'General Cargo'),
            ('hazardous', 'Hazardous'),
            ('reefer', 'Reefer'),
            ('special', 'Special')
        ],
        string='Cargo Type'
    )

    def _build_domain(self):
        self.ensure_one()
        domain = []

        if self.company_id:
            domain.append(('company_id', '=', self.company_id.id))

        if self.branch_id:
            domain.append(('branch_id', '=', self.branch_id.id))

        if self.date_from:
            domain.append(('hbl_date', '>=', self.date_from))

        if self.date_to:
            domain.append(('hbl_date', '<=', self.date_to))

        if self.shipper_id:
            domain.append(('hbl_consigner_id', '=', self.shipper_id.id))

        if self.consignee_id:
            domain.append(('hbl_consignee_id', '=', self.consignee_id.id))

        if self.shipping_line_id:
            domain.append(('hbl_carrier_id', '=', self.shipping_line_id.id))

        if self.destination_agent_id:
            domain.append(('hbl_destagent_id', '=', self.destination_agent_id.id))

        if self.load_port_id:
            domain.append(('hbl_portload_id', '=', self.load_port_id.id))

        if self.discharge_port_id:
            domain.append(('hbl_portdisch_id', '=', self.discharge_port_id.id))

        if self.consol_type:
            domain.append(('type_id', '=', self.consol_type))

        if self.cargo_type:
            domain.append(('hbl_movtype', '=', self.cargo_type))

        return domain

    def action_export_xlsx(self):
        self.ensure_one()

        data = {
            'domain': self._build_domain(),
            'date_from': self.date_from,
            'date_to': self.date_to,
            'branch_name': self.branch_id.name if self.branch_id else '',
        }

        return self.env.ref(
            'shipping_report.shipping_report_shipment_revenue_xlsx'
        ).report_action(self, data=data)