# # -*- coding: utf-8 -*-
# from odoo import models, fields, api
# from odoo.exceptions import ValidationError
# from datetime import date, datetime, time, timedelta
# from dateutil.relativedelta import relativedelta
#
#
# class ShipmentRevenueWizard(models.TransientModel):
#     _name = 'shipment.revenue.wizard'
#     _description = 'Sea Export Shipment Register - Revenue'
#
#     date_filter = fields.Selection(
#         [
#             ('today', 'Today'),
#             ('yesterday', 'Yesterday'),
#             ('this_week', 'This Week'),
#             ('last_week', 'Last Week'),
#             ('this_month', 'This Month'),
#             ('last_month', 'Last Month'),
#             ('this_year', 'This Year'),
#             ('custom', 'Custom Range'),
#         ],
#         string="Date Range",
#         default='this_month'
#     )
#
#     date_from = fields.Date(
#         string='Shipment Date From',
#         required=True,
#         default=lambda self: fields.Date.today().replace(day=1)
#     )
#     date_to = fields.Date(
#         string='Shipment Date To',
#         required=True,
#         default=fields.Date.today
#     )
#
#     branch_id = fields.Many2one(
#         'res.company',
#         string='Branch',
#         required=True
#     )
#
#     @api.model
#     def default_get(self, fields_list):
#         res = super().default_get(fields_list)
#         branch = self.env.user.branch_ids[:1]
#         if branch:
#             res['branch_id'] = branch.id
#         return res
#
#     shipper_id = fields.Many2one(
#         'res.partner',
#         string='Shipper',
#         domain=[('is_company', '=', True)]
#     )
#     consignee_id = fields.Many2one(
#         'res.partner',
#         string='Consignee',
#         domain=[('is_company', '=', True)]
#     )
#     shipping_line_id = fields.Many2one(
#         'res.partner',
#         string='Shipping Line',
#         domain=[('is_company', '=', True)]
#     )
#     destination_agent_id = fields.Many2one(
#         'res.partner',
#         string='Destination Agent',
#         domain=[('is_company', '=', True)]
#     )
#
#     load_port_id = fields.Many2one('res.partner', string='Load Port')
#     discharge_port_id = fields.Many2one('res.partner', string='Discharge Port')
#
#     consol_type = fields.Selection(
#         [('fcl', 'FCL'), ('lcl', 'LCL'), ('breakbulk', 'Break Bulk')],
#         string='Consol Type'
#     )
#     cargo_type = fields.Selection(
#         [
#             ('general', 'General Cargo'),
#             ('hazardous', 'Hazardous'),
#             ('reefer', 'Reefer'),
#             ('special', 'Special')
#         ],
#         string='Cargo Type'
#     )
#
#     @api.onchange("date_filter")
#     def _onchange_date_filter(self):
#         today = date.today()
#
#         if self.date_filter == "today":
#             self.date_from = today
#             self.date_to = today
#
#         elif self.date_filter == "yesterday":
#             y = today - timedelta(days=1)
#             self.date_from = y
#             self.date_to = y
#
#         elif self.date_filter == "this_week":
#             start = today - timedelta(days=today.weekday())
#             self.date_from = start
#             self.date_to = start + timedelta(days=6)
#
#         elif self.date_filter == "last_week":
#             start = today - timedelta(days=today.weekday() + 7)
#             self.date_from = start
#             self.date_to = start + timedelta(days=6)
#
#         elif self.date_filter == "this_month":
#             start = today.replace(day=1)
#             self.date_from = start
#             self.date_to = start + relativedelta(months=1, days=-1)
#
#         elif self.date_filter == "last_month":
#             last_day = today.replace(day=1) - timedelta(days=1)
#             self.date_from = last_day.replace(day=1)
#             self.date_to = last_day
#
#         elif self.date_filter == "this_year":
#             self.date_from = today.replace(month=1, day=1)
#             self.date_to = today.replace(month=12, day=31)
#
#     @api.constrains("date_from", "date_to")
#     def _check_date(self):
#         for rec in self:
#             if rec.date_from and rec.date_to and rec.date_from > rec.date_to:
#                 raise ValidationError("From Date cannot be after To Date")
#
#     def action_generate_report(self):
#         self.ensure_one()
#         return {
#             'name': 'Sea Export Shipment Register - Revenue',
#             'type': 'ir.actions.act_window',
#             'res_model': 'ship.shipment',
#             'view_mode': 'tree,form',
#             'domain': self._build_domain(),
#             'context': {'create': False, 'edit': False},
#             'target': 'current',
#         }
#
#     def _build_domain(self):
#
#         domain = []
#
#
#         if self.date_from:
#             domain.append(('hbl_date', '>=', self.date_from))
#         if self.date_to:
#             domain.append(('hbl_date', '<=', self.date_to))
#
#
#         if self.branch_id:
#             domain.append(('branch_id', '=', self.branch_id.id))
#
#
#         if self.shipper_id:
#             domain.append(('hbl_shipper_id', '=', self.shipper_id.id))
#         if self.consignee_id:
#             domain.append(('hbl_consignee_id', '=', self.consignee_id.id))
#         if self.shipping_line_id:
#             domain.append(('shipping_line_id', '=', self.shipping_line_id.id))
#         if self.destination_agent_id:
#             domain.append(('destination_agent_id', '=', self.destination_agent_id.id))
#         if self.load_port_id:
#             domain.append(('port_of_load_id', '=', self.load_port_id.id))
#         if self.discharge_port_id:
#             domain.append(('port_of_discharge_id', '=', self.discharge_port_id.id))
#         if self.consol_type:
#             domain.append(('consol_type', '=', self.consol_type))
#         if self.cargo_type:
#             domain.append(('cargo_type', '=', self.cargo_type))
#
#         return domain
#
#     def action_clear_filters(self):
#         self.write({
#             'shipper_id': False,
#             'consignee_id': False,
#             'shipping_line_id': False,
#             'destination_agent_id': False,
#             'load_port_id': False,
#             'discharge_port_id': False,
#             'consol_type': False,
#             'cargo_type': False,
#         })
#         return {'type': 'ir.actions.do_nothing'}
#
#     def action_export_xlsx(self):
#
#         self.ensure_one()
#
#
#         data = {
#             'domain': self._build_domain(),
#             'date_from': self.date_from,
#             'date_to': self.date_to,
#             'branch_name': self.branch_id.name if self.branch_id else '',
#         }
#
#         return {
#             'type': 'ir.actions.report',
#             'report_type': 'xlsx',
#             'report_name': 'shipment_revenue.shipment_revenue_xlsx',
#             'report_file': 'Sea_Export_Shipment_Register_Revenue',
#             'data': data,
#         }# -*- coding: utf-8 -*-
# from odoo import models, fields, api
# from odoo.exceptions import ValidationError
# from datetime import date, timedelta
# from dateutil.relativedelta import relativedelta
#
#
# class ShipmentRevenueWizard(models.TransientModel):
#     _name = 'shipment.revenue.wizard'
#     _description = 'Sea Export Shipment Register - Revenue'
#
#     date_filter = fields.Selection(
#         [
#             ('today', 'Today'),
#             ('yesterday', 'Yesterday'),
#             ('this_week', 'This Week'),
#             ('last_week', 'Last Week'),
#             ('this_month', 'This Month'),
#             ('last_month', 'Last Month'),
#             ('this_year', 'This Year'),
#             ('custom', 'Custom Range'),
#         ],
#         string="Date Range",
#         default='this_month'
#     )
#
#     date_from = fields.Date(
#         string='Shipment Date From',
#         required=True,
#         default=lambda self: fields.Date.today().replace(day=1)
#     )
#     date_to = fields.Date(
#         string='Shipment Date To',
#         required=True,
#         default=fields.Date.today
#     )
#
#     branch_id = fields.Many2one(
#         'res.company',
#         string='Branch',
#         required=True
#     )
#
#     @api.model
#     def default_get(self, fields_list):
#         res = super().default_get(fields_list)
#         branch = self.env.user.branch_ids[:1]
#         if branch:
#             res['branch_id'] = branch.id
#         return res
#
#     shipper_id = fields.Many2one(
#         'res.partner',
#         string='Shipper',
#         domain=[('is_company', '=', True)]
#     )
#     consignee_id = fields.Many2one(
#         'res.partner',
#         string='Consignee',
#         domain=[('is_company', '=', True)]
#     )
#     shipping_line_id = fields.Many2one(
#         'res.partner',
#         string='Shipping Line',
#         domain=[('is_company', '=', True)]
#     )
#     destination_agent_id = fields.Many2one(
#         'res.partner',
#         string='Destination Agent',
#         domain=[('is_company', '=', True)]
#     )
#
#     load_port_id = fields.Many2one(
#         'ship.port',
#         string='Load Port',
#         store=False
#     )
#
#     discharge_port_id = fields.Many2one(
#         'ship.port',
#         string='Discharge Port',
#         store=False
#     )
#
#     consol_type = fields.Selection(
#         [('fcl', 'FCL'), ('lcl', 'LCL'), ('breakbulk', 'Break Bulk')],
#         string='Consol Type'
#     )
#
#     cargo_type = fields.Selection(
#         [
#             ('general', 'General Cargo'),
#             ('hazardous', 'Hazardous'),
#             ('reefer', 'Reefer'),
#             ('special', 'Special')
#         ],
#         string='Cargo Type'
#     )
#
#     @api.onchange("date_filter")
#     def _onchange_date_filter(self):
#         today = date.today()
#
#         if self.date_filter == "today":
#             self.date_from = today
#             self.date_to = today
#
#         elif self.date_filter == "yesterday":
#             y = today - timedelta(days=1)
#             self.date_from = y
#             self.date_to = y
#
#         elif self.date_filter == "this_week":
#             start = today - timedelta(days=today.weekday())
#             self.date_from = start
#             self.date_to = start + timedelta(days=6)
#
#         elif self.date_filter == "last_week":
#             start = today - timedelta(days=today.weekday() + 7)
#             self.date_from = start
#             self.date_to = start + timedelta(days=6)
#
#         elif self.date_filter == "this_month":
#             start = today.replace(day=1)
#             self.date_from = start
#             self.date_to = start + relativedelta(months=1, days=-1)
#
#         elif self.date_filter == "last_month":
#             last_day = today.replace(day=1) - timedelta(days=1)
#             self.date_from = last_day.replace(day=1)
#             self.date_to = last_day
#
#         elif self.date_filter == "this_year":
#             self.date_from = today.replace(month=1, day=1)
#             self.date_to = today.replace(month=12, day=31)
#
#     @api.constrains("date_from", "date_to")
#     def _check_date(self):
#         for rec in self:
#             if rec.date_from and rec.date_to and rec.date_from > rec.date_to:
#                 raise ValidationError("From Date cannot be after To Date")
#
#     def _build_domain(self):
#         domain = []
#
#         if self.date_from:
#             domain.append(('hbl_date', '>=', self.date_from))
#         if self.date_to:
#             domain.append(('hbl_date', '<=', self.date_to))
#
#         if self.branch_id:
#             domain.append(('branch_id', '=', self.branch_id.id))
#
#         if self.shipper_id:
#             domain.append(('hbl_consigner_id', '=', self.shipper_id.id))
#
#         if self.consignee_id:
#             domain.append(('hbl_consignee_id', '=', self.consignee_id.id))
#
#         if self.shipping_line_id:
#             domain.append(('hbl_carrier_id', '=', self.shipping_line_id.id))
#
#         if self.destination_agent_id:
#             domain.append(('hbl_destagent_id', '=', self.destination_agent_id.id))
#
#         if self.load_port_id:
#             domain.append(('hbl_portload_id', '=', self.load_port_id.id))
#
#         if self.discharge_port_id:
#             domain.append(('hbl_portdisch_id', '=', self.discharge_port_id.id))
#
#         # ❌ consol_type REMOVED (not a field on ship.shipment)
#
#         if self.cargo_type:
#             domain.append(('cargo_type', '=', self.cargo_type))
#
#         return domain
#
#     def action_export_xlsx(self):
#         self.ensure_one()
#
#         data = {
#             'domain': self._build_domain(),
#             'date_from': self.date_from,
#             'date_to': self.date_to,
#             'branch_name': self.branch_id.name if self.branch_id else '',
#         }
#
#         return {
#             'type': 'ir.actions.report',
#             'report_type': 'xlsx',
#             'report_name': 'shipment_revenue.shipment_revenue_xlsx',
#             'report_file': 'Sea_Export_Shipment_Register_Revenue',
#             'data': data,
#         }
# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta


class ShipmentRevenueWizard(models.TransientModel):
    _name = 'shipment.revenue.wizard'
    _description = 'Sea Export Shipment Register - Revenue'

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
        string='Shipment Date From',
        required=True,
        default=lambda self: fields.Date.today().replace(day=1)
    )
    date_to = fields.Date(
        string='Shipment Date To',
        required=True,
        default=fields.Date.today
    )

    branch_id = fields.Many2one(
        'res.company',
        string='Branch',
        required=True
    )

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        branch = self.env.user.branch_ids[:1]
        if branch:
            res['branch_id'] = branch.id
        return res

    shipper_id = fields.Many2one(
        'res.partner',
        string='Shipper',
        domain=[('is_company', '=', True)]
    )
    consignee_id = fields.Many2one(
        'res.partner',
        string='Consignee',
        domain=[('is_company', '=', True)]
    )
    shipping_line_id = fields.Many2one(
        'res.partner',
        string='Shipping Line',
        domain=[('is_company', '=', True)]
    )
    destination_agent_id = fields.Many2one(
        'res.partner',
        string='Destination Agent',
        domain=[('is_company', '=', True)]
    )

    load_port_id = fields.Many2one(
        'ship.port',
        string='Load Port',
        store=False
    )

    discharge_port_id = fields.Many2one(
        'ship.port',
        string='Discharge Port',
        store=False
    )

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

    def _build_domain(self):
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

        if self.shipping_line_id:
            domain.append(('hbl_carrier_id', '=', self.shipping_line_id.id))

        if self.destination_agent_id:
            domain.append(('hbl_destagent_id', '=', self.destination_agent_id.id))

        if self.load_port_id:
            domain.append(('hbl_portload_id', '=', self.load_port_id.id))

        if self.discharge_port_id:
            domain.append(('hbl_portdisch_id', '=', self.discharge_port_id.id))



        if self.cargo_type:
            domain.append(('cargo_type', '=', self.cargo_type))

        return domain

    def action_export_xlsx(self):
        self.ensure_one()

        data = {
            'domain': self._build_domain(),
            'date_from': self.date_from,
            'date_to': self.date_to,
            'branch_name': self.branch_id.name if self.branch_id else '',
        }

        return {
            'type': 'ir.actions.report',
            'report_type': 'xlsx',
            'report_name': 'shipment_revenue.shipment_revenue_xlsx',
            'report_file': 'Sea_Export_Shipment_Register_Revenue',
            'data': data,
        }
