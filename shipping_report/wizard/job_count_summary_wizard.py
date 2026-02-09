# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta


class JobCountSummaryWizard(models.TransientModel):
    _name = 'job.count.summary.wizard'
    _description = 'Job Count Summary Wizard'

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
        string='Job Opened From',
        required=True,
        default=lambda self: fields.Date.today().replace(day=1)
    )
    date_to = fields.Date(
        string='Job Opened To',
        required=True,
        default=fields.Date.today
    )

    branch_id = fields.Many2one(
        'res.company',
        string='Branch'
    )

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        branch = self.env.user.branch_ids[:1]
        if branch:
            res['branch_id'] = branch.id
        return res

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

    def action_print_pdf(self):

        self.ensure_one()
        return self.env.ref('job_count_summary.job_count_summary_pdf').report_action(self)

    def action_export_xlsx(self):

        self.ensure_one()

        data = {
            'wizard_id': self.id,
            'date_from': self.date_from,
            'date_to': self.date_to,
            'branch_name': self.branch_id.name if self.branch_id else 'All Branches',
        }

        return {
            'type': 'ir.actions.report',
            'report_type': 'xlsx',
            'report_name': 'job_count_summary.job_count_summary_xlsx',
            'report_file': 'Job_Count_Summary',
            'data': data,
        }

    def _get_report_data(self):

        self.ensure_one()


        domain = [
            ('hbl_date', '>=', self.date_from),
            ('hbl_date', '<=', self.date_to),
        ]

        if self.branch_id:
            domain.append(('branch_id', '=', self.branch_id.id))


        shipments = self.env['ship.shipment'].search(domain, order='branch_id, hbl_date')


        branches_data = {}
        grand_totals = {
            'accounting_job_headers': 0,
            'job_headers_on_shipments': 0,
            'job_headers_standalone': 0,
            'job_headers_with_declarations': 0,
            'shipment_fcl_teu': 0.0,
            'shipment_chargeable_wv': 0.0,
            'shipment_air_kg': 0.0,
        }


        for ship in shipments:

            if ship.branch_id:
                branch_code = ship.branch_id.code if hasattr(ship.branch_id, 'code') and ship.branch_id.code else ship.branch_id.name[:3].upper()
                branch_name = ship.branch_id.name
            else:
                branch_code = 'UNK'
                branch_name = 'Unknown'


            if hasattr(ship, 'department_id') and ship.department_id:
                department = ship.department_id.code if hasattr(ship.department_id, 'code') else ship.department_id.name
            else:
                department = 'N/A'

            if hasattr(ship, 'freight_direction'):
                freight_dir = ship.freight_direction.upper() if ship.freight_direction else 'N/A'
            elif hasattr(ship, 'service_type'):
                freight_dir = ship.service_type.upper() if ship.service_type else 'N/A'
            else:
                freight_dir = 'N/A'

            if hasattr(ship, 'transport_mode'):
                trans_mode = ship.transport_mode.upper() if ship.transport_mode else 'N/A'
            elif hasattr(ship, 'consol_type'):
                trans_mode = ship.consol_type.upper() if ship.consol_type else 'N/A'
            else:
                trans_mode = 'N/A'

            if branch_code not in branches_data:
                branches_data[branch_code] = {
                    'branch_code': branch_code,
                    'branch_name': branch_name,
                    'rows': {},
                    'totals': {
                        'accounting_job_headers': 0,
                        'job_headers_on_shipments': 0,
                        'job_headers_standalone': 0,
                        'job_headers_with_declarations': 0,
                        'shipment_fcl_teu': 0.0,
                        'shipment_chargeable_wv': 0.0,
                        'shipment_air_kg': 0.0,
                    }
                }


            row_key = f"{department}|{freight_dir}|{trans_mode}"


            if row_key not in branches_data[branch_code]['rows']:
                branches_data[branch_code]['rows'][row_key] = {
                    'department': department,
                    'freight_direction': freight_dir,
                    'transport_mode': trans_mode,
                    'accounting_job_headers': 0,
                    'job_headers_on_shipments': 0,
                    'job_headers_standalone': 0,
                    'job_headers_with_declarations': 0,
                    'shipment_fcl_teu': 0.0,
                    'shipment_chargeable_wv': 0.0,
                    'shipment_air_kg': 0.0,
                }

            row = branches_data[branch_code]['rows'][row_key]


            row['accounting_job_headers'] += 1
            row['job_headers_on_shipments'] += 1

            if hasattr(ship, 'consol_type'):
                if ship.consol_type == 'fcl' and hasattr(ship, 'total_teu'):
                    row['shipment_fcl_teu'] += ship.total_teu or 0.0
                elif ship.consol_type == 'fcl' and hasattr(ship, 'container_count'):
                    row['shipment_fcl_teu'] += ship.container_count or 0.0

            if hasattr(ship, 'chargeable_weight'):
                row['shipment_chargeable_wv'] += ship.chargeable_weight or 0.0
            elif hasattr(ship, 'total_weight'):
                row['shipment_chargeable_wv'] += ship.total_weight or 0.0

            if hasattr(ship, 'gross_weight'):
                row['shipment_air_kg'] += ship.gross_weight or 0.0

            for key in row:
                if key not in ['department', 'freight_direction', 'transport_mode']:
                    branches_data[branch_code]['totals'][key] += row[key]

        branches_list = []
        for branch_code in sorted(branches_data.keys()):
            branch_data = branches_data[branch_code]
            # Convert rows dict to list and sort
            branch_data['rows'] = sorted(
                branch_data['rows'].values(),
                key=lambda x: (x['department'], x['freight_direction'], x['transport_mode'])
            )
            branches_list.append(branch_data)

            for key, value in branch_data['totals'].items():
                grand_totals[key] += value

        return {
            'date_from': self.date_from,
            'date_to': self.date_to,
            'branch_name': self.branch_id.name if self.branch_id else 'All Branches',
            'branches': branches_list,
            'grand_total': grand_totals,
        }

    def action_export_xlsx(self):
        self.ensure_one()
        return self.env.ref(
            'job_count_summary.job_count_summary_xlsx'
        ).report_action(self)
