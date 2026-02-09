from odoo import models, fields, api
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta


class ShipReportWizard(models.TransientModel):
    _name = "ship.report.wizard"
    _description = "Job Profit Report"

    date_from = fields.Date(required=True, default=lambda self: date.today().replace(day=1))
    date_to = fields.Date(required=True, default=lambda self: date.today())

    date_filter = fields.Selection([
        ('today', 'Today'),
        ('yesterday', 'Yesterday'),
        ('this_week', 'This Week'),
        ('this_month', 'This Month'),
        ('last_month', 'Last Month'),
        ('this_year', 'This Year'),
        ('custom', 'Custom Range')
    ], default='this_month')

    branch_id = fields.Many2one(
        'res.company',
        string="Branch",
        domain="[('parent_id','!=',False)]"
    )

    department_id = fields.Many2one('ship.department', string="Department")
    carrier_id = fields.Many2one('ship.carriers', string="Carrier")

    report_type = fields.Selection([
        ('summary', 'Summary By Job'),
        ('detail', 'Transaction Detail'),
    ], default='summary')

    @api.onchange("date_filter")
    def _onchange_date_filter(self):
        today = date.today()
        if self.date_filter == "today":
            self.date_from = self.date_to = today
        elif self.date_filter == "yesterday":
            self.date_from = self.date_to = today - timedelta(days=1)
        elif self.date_filter == "this_week":
            self.date_from = today - timedelta(days=today.weekday())
            self.date_to = self.date_from + timedelta(days=6)
        elif self.date_filter == "this_month":
            self.date_from = today.replace(day=1)
            self.date_to = self.date_from + relativedelta(months=1, days=-1)
        elif self.date_filter == "last_month":
            first = today.replace(day=1)
            last = first - timedelta(days=1)
            self.date_from = last.replace(day=1)
            self.date_to = last
        elif self.date_filter == "this_year":
            self.date_from = today.replace(month=1, day=1)
            self.date_to = today.replace(month=12, day=31)

    def _get_data(self):
        summary = []
        details = {}

        domain = [
            ('hbl_date', '>=', self.date_from),
            ('hbl_date', '<=', self.date_to),
        ]

        if self.branch_id:
            domain.append(('branch_id', '=', self.branch_id.id))

        if self.department_id:
            domain.append(('department_id', '=', self.department_id.id))

        if self.carrier_id:
            domain.append(('hbl_carrier_id', '=', self.carrier_id.id))

        shipments = self.env['ship.shipment'].search(domain)

        if self.report_type == 'summary':
            for sh in shipments:
                revenue = sum(sh.hbl_charges_ids.mapped('amount_sell'))
                cost = sum(sh.hbl_charges_ids.mapped('amount_cost'))
                wip = sum(sh.hbl_charges_ids.mapped('os_sell'))
                accrual = sum(sh.hbl_charges_ids.mapped('os_cost'))

                summary.append({
                    'job': sh.name or '',
                    'ref': sh.name or '',
                    'branch': sh.branch_id.name if sh.branch_id else '',
                    'dept': sh.department_id.name if sh.department_id else '',
                    'status': sh.state or '',
                    'trans': sh.mode_id.name if sh.mode_id else '',
                    'cont': '',
                    'sales': sh.employee_id.name if sh.employee_id else '',
                    'client': sh.hbl_customer_id.name if sh.hbl_customer_id else '',
                    'origin': sh.hbl_portload_id.code if sh.hbl_portload_id else '',
                    'dest': sh.hbl_portdisch_id.code if sh.hbl_portdisch_id else '',
                    'etd': sh.hbl_depdate,
                    'eta': sh.hbl_arrivaldt,
                    'revenue': revenue,
                    'wip': wip,
                    'cost': cost,
                    'accrual': accrual,
                    'profit': revenue - cost,
                })

            return summary, {}

        details = {}

        for sh in shipments:
            lines = []

            for ch in sh.hbl_charges_ids:
                lines.append({
                    'type': sh.mode_id.name if sh.mode_id else '',
                    'charge': ch.charge_id.name if ch.charge_id else '',
                    'posted': sh.hbl_date,
                    'br': sh.company_id.name if sh.company_id else '',
                    'dept': sh.department_id.name if sh.department_id else '',
                    'org': sh.hbl_carrier_id.name if sh.hbl_carrier_id else '',
                    'invoice': '',  # YOU DO NOT HAVE INVOICE LINK – keep empty
                    'amount': ch.amount or 0.0,
                    'job_profit': (ch.amount_sell or 0.0) - (ch.amount_cost or 0.0),
                    'revenue': ch.amount_sell or 0.0,
                    'wip': ch.os_sell or 0.0,
                    'cost': ch.amount_cost or 0.0,
                    'accrual': ch.os_cost or 0.0,
                })

            if lines:
                details[sh.id] = lines

        return [], details

    def action_print_pdf(self):
        return self.env.ref('shipping_report.ship_report_pdf_action').report_action(self)

    def action_export_xlsx(self):
        return self.env.ref('shipping_report.ship_report_xlsx_action').report_action(self)