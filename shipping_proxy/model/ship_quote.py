# from google.protobuf.text_encoding import string
# from google.auth import default
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from datetime import timedelta
import logging
import base64

_logger = logging.getLogger(__name__)


class ShippingQuote(models.Model):
    _name = "ship.quote"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Quotation"
    _rec_name = 'name'

    # name = fields.Char(string="Quote Number", Required=True, copy=False, readonly=False, tracking=True,
    #                    default=lambda self: _('New'))
    name = fields.Char(
        string='Quote Number',
        required=True,
        copy=False,
        readonly=True,
        index=True,
        default='/'
    )
    mode_id = fields.Many2one('ship.mode', related='department_id.mode_id', string='Mode', store=True)
    transport_id = fields.Many2one('ship.transport', related='department_id.transport_id', string='Transport', store=True)
    transport_code = fields.Char('ship.transport', related='transport_id.code')
    type_id = fields.Many2one('ship.type', string='Type')
    add_terms = fields.Char(string='Add Terms')
    # mode = fields.Char(related="mode_id.code")
    service_id = fields.Many2one('ship.servicelevel',string ='Service Level')
    container_id = fields.Many2one('ship.container', string='Container')
    quote_date = fields.Date(string='Date',default=fields.Date.context_today)
    company_id = fields.Many2one('res.company', string='Company', readonly=True, default=lambda self: self.env.company)
    branch_id = fields.Many2one('res.company', string='Branch', readonly=True)
    department_id = fields.Many2one('ship.department', string='Department', readonly=True,store=True)
    company_code = fields.Char(string="Company Code")
    branch_code = fields.Char(string="Branch Code")
    # department_code = fields.Char(string="Department Code")
    # branch_id = fields.Integer(default='1')
    # company_id = fields.Many2one('res.company', required=True, default=lambda r: r.env.company)

    quote_startdt = fields.Date(string='Start Date',default=fields.Date.context_today)
    qutoe_enddt = fields.Date(string='End Date',compute='_compute_end_date',
        store=True)

    client_id = fields.Many2one('res.partner', string='Client', required=True, domain=[('customer_rank', '>', 0)])

    client_street = fields.Char(related='client_id.street',string='Client Street', store=False)
    client_street2 = fields.Char(related='client_id.street2',string='Client Street2', store=False)
    client_zip_code = fields.Char(related='client_id.zip',string='Client ZIP Code', store=False)
    client_city = fields.Char(related='client_id.city',string='Client City', store=False)
    client_state_id = fields.Many2one(related='client_id.state_id',string="Client State", store=False)
    client_country_id = fields.Many2one(related='client_id.country_id', string="Client Country", store=False)

    consignor_id = fields.Many2one('res.partner', string='Consigner', required=True, domain="[('consigner', '=', True)]")

    consignor_street = fields.Char(related='consignor_id.street',string='Consigner Street', store=False)
    consignor_street2 = fields.Char(related='consignor_id.street2',string='Consigner Street2', store=False)
    consignor_zip_code = fields.Char(related='consignor_id.zip',string='Consigner ZIP Code', store=False)
    consignor_city = fields.Char(related='consignor_id.city',string='Consigner City', store=False)
    consignor_state_id = fields.Many2one(related='consignor_id.state_id', string="Consigner State", store=False)
    consignor_country_id = fields.Many2one(related='consignor_id.country_id', string="Consigner Country", store=False)

    consignee_id = fields.Many2one('res.partner', string='Consignee',
                                   domain="[('consignee', '=', True)]")
    consignee_street = fields.Char(related='consignee_id.street',string='Consignee Street', store=False)
    consignee_street2 = fields.Char(related='consignee_id.street2',string='Consignee Street2', store=False)
    consignee_zip_code = fields.Char(related='consignee_id.city',string='Consignee ZIP Code', store=False)
    consignee_city = fields.Char(related='consignee_id.city',string='Consignee City', store=False)
    consignee_state_id = fields.Many2one(related='consignee_id.state_id', string="Consignee State", store=False)
    consignee_country_id = fields.Many2one(related='consignee_id.country_id', string="Consignee Country", store=False)

    employee_id = fields.Many2one('res.users', string='Sales Person', required=True)
    agent_id = fields.Many2one('res.partner', string='Agent', domain="[('forward_agent', '=', True)]")
    code = fields.Many2one('ship.department', string='Deparment')
    inco_id = fields.Many2one('ship.salesterms', string='Inco Terms', required=True)

    orgin_id = fields.Many2one('ship.port', string='Origin', required=True)
    dest_id = fields.Many2one('ship.port', string="Destination", required=True)
    final_id = fields.Many2one('ship.port', string="Final Destination")
    via_id = fields.Many2one('ship.port', string='Via')
    # carrier_id = fields.Many2one('ship.carriers', string='Carrier')
    transit_time = fields.Integer(string='Transit Time')
    package_id = fields.Many2many('ship.packagetype', string='Package Type')
    quote_weight = fields.Float(string='Weight')
    weight_uom = fields.Selection([
        ('g', 'Gram'),
        ('kg', 'Kilogram')
    ], string='Weight Unit', default='kg')
    quote_volume = fields.Float(string='Volume')
    volume_uom = fields.Selection([
        ('m3', 'CM3'),
    ], string='Volume Unit', default='m3')
    quote_chargable = fields.Float(string='Chargable')
    goods_value = fields.Float(string='Goods Value')
    insur_value = fields.Float(string='Insured Value')
    commodity_id = fields.Many2one('ship.commodity', string='Commodity',size=50)
    picdrop = fields.Boolean(string='Pick / Drop')
    currency_id = fields.Many2one('res.currency', 'Çurrency', required=True,
                                  default=lambda self: self.env.company.currency_id)
    country_origin = fields.Many2one('res.country', string='Country of origin')
    dg_applicable = fields.Boolean(string="DG")
    dg_class = fields.Char(string='Classification')
    delivery_id = fields.Many2one('ship.delivery', string='Delivery Mode')

    # quotefcl_ids = fields.One2many('ship.quote.fcl', 'fcl_id', string='FCL Container details')
    # quotelcl_ids = fields.One2many('ship.quote.lcl', 'lcl_id', string='LCL Container details')
    crg_cargo_ids = fields.One2many('ship.quote.cargo', 'crg_cargo_id', string='Cargo Details')
    quoteshpline_ids = fields.One2many('ship.quote.line', 'line_id', string='Shipping Line Details')
    state = fields.Selection([
        ('draft', 'Draft'),
        # ('quote', 'Quote Sent'),
        ('confirm', 'Confirmed'),
        ('booking', 'Booking'),
        ('cancel', 'Cancelled'),
        # Add more states as needed
    ], string='Status', default='draft')

    tax_totals = fields.Binary(compute='_compute_tax_totals', exportable=False)
    booking_count = fields.Integer(compute='compute_booking')
    company_desc = fields.Char(string='Company ', compute="_compute_company_description", store=True)

    total_income = fields.Monetary(
        string="Total Income",
        compute="_compute_totals",
        store=True,
        currency_field='currency_id'
    )
    total_expense = fields.Monetary(
        string="Total Expense",
        compute="_compute_totals",
        store=True,
        currency_field='currency_id'
    )
    total_profit_loss = fields.Monetary(
        string="Total Profit/Loss",
        compute="_compute_totals",
        store=True,
        currency_field='currency_id'
    )
    total_profit_loss_percentage = fields.Float(
        string="Total Profit/Loss %",
        compute="_compute_totals",
        store=True
    )


class ShipShipcargo(models.Model):
    _name = "ship.quote.cargo"
    _description = "Shipment Cargo Details"

    # Container Details

    quote_id = fields.Many2one('ship.quote', string='Quote')
    transport_id = fields.Many2one('shipping.transport', string='Transport', related='quote_id.transport_id',
                                   store=False)
    crg_container = fields.Char(string='Container')
    crg_contno = fields.Char(string='Container No')
    crg_sealno = fields.Char(string='Seal No')
    crg_conttype_id = fields.Many2one('ship.containertype', string='Continer Type')
    crg_delvtype = fields.Selection([
        ('gen', 'GEN'),
        ('dgr', 'DGR'),
        ('oog', 'OOG'),

    ], string='Delivery Type', default='gen')
    crg_fe = fields.Char(string='F/E')

    # Commodity Details

    crg_packtype_id = fields.Many2one('ship.packagetype', string='Package Type')
    crg_pieces = fields.Integer(string='Pieces')
    crg_commod_id = fields.Many2one('ship.commodity', string='Çommodity')
    crg_hscode = fields.Char(string='HS Code')
    crg_marksno = fields.Char(string='Marks & Numbers')
    crg_danger = fields.Boolean(string='Dangerous Goods')
    crg_imdgno = fields.Char(string='ÍMDG No')
    crg_umno = fields.Char(string='ÚM No')
    crg_length = fields.Float(string='Length', related='crg_conttype_id.length', store=True)
    crg_length_id = fields.Selection([
        ('cent', 'Centimeter'),
        ('mtr', 'Meter'), ], string='Length Uom', default='mtr')
    crg_height = fields.Float(string='Height', related='crg_conttype_id.height', store=True)
    crg_height_id = fields.Selection([
        ('cent', 'Centimeter'),
        ('mtr', 'Meter'), ], string='Height Uom', default='mtr')
    crg_width = fields.Float(string='Width No ', related='crg_conttype_id.width', store=True)
    crg_width_id = fields.Selection([
        ('cent', 'Centimeter'),
        ('mtr', 'Meter'), ], string='Width Uom', default='mtr')
    crg_weight = fields.Float(string='Weight', related='crg_conttype_id.weight', store=True)
    crg_weight_id = fields.Selection([
        ('kgm', 'KGM'), ], string='Weight Uom', default='kgm')
    crg_volume = fields.Float(string='Volume', related='crg_conttype_id.volume', store=True)
    crg_volume_id = fields.Selection([
        ('m3', 'M3'), ], string='Vol Weight Uom', default='m3')

    crg_cargo_id = fields.Many2one('ship.quote', string='Cargo Details')



class ShipQuoteLine(models.Model):
    _name = "ship.quote.line"
    _description = "Shipping Line"

    line_id = fields.Many2one('ship.quote')
    shipline_id = fields.Many2one('ship.carriers', string='Carrier Name')
    selected = fields.Boolean('Selected')
    shiplinecharge_ids = fields.One2many('ship.line.charges', 'line_charge_id', string='Shipping Charges')
    currency_id = fields.Many2one('res.currency', 'Çurrency', required=True,
                                  default=lambda self: self.env.company.currency_id)
    income = fields.Monetary(string='Income', compute='_compute_income_expense',store=True)
    expense = fields.Monetary(string='Expense', compute='_compute_income_expense' ,store=True)
    profit_loss = fields.Monetary(string='Profit/Loss', compute='_compute_profit_loss' ,store=True)
    profit_loss_percentage = fields.Float(string='Profit/Loss %', compute='_compute_profit_loss' ,store=True)

    quote_id = fields.Many2one('ship.quote', string="Quote")
    transport_id = fields.Many2one(
        related='quote_id.transport_id',
        store=True,
        string="Transport"
    )
    mode_id = fields.Many2one(
        related='quote_id.mode_id',
        store=True,
        string="Mode"
    )
    container_id = fields.Many2one(
        related='quote_id.container_id',
        store=True,
        string="Container"
    )

class ShipLineCharges(models.Model):
    _name = "ship.line.charges"
    _description = "Shipping Line Charges"

    line_charge_id = fields.Many2one('ship.quote.line')
    ship_quote_id = fields.Many2one('ship.quote')

    charge_id = fields.Many2one('product.product', string='Charge', required=True)
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        required=True,
        default=lambda self: self.env.company.currency_id)

    company_currency_id = fields.Many2one('res.currency', string="Company Currency",
                                          default=lambda self: self.env.company.currency_id)
    cost_currency_id = fields.Many2one('res.currency', string="Cost Currency",
                                       store=True,default=lambda self: self.env.company.currency_id)
    os_cost = fields.Monetary(string='OS Cost', currency_field='currency_id', readonly=True)
    estimated_cost = fields.Monetary(string='Estimated Cost', currency_field='currency_id')
    local_cost = fields.Monetary(string='Local Cost', currency_field='currency_id', compute="_compute_local_costs",
                                 store=True)
    creditor_id = fields.Many2one('res.partner', string="Creditor",store=True)

    cost_tax_id = fields.Many2many(
        'account.tax',
        'ship_line_charges_tax_rel',
        'charge_id',
        'tax_id',
        string='Cost Tax',compute="_compute_tax_ids")
    # cost_tax_id = fields.Many2many('account.tax', string='Tax')
    cost_tax_amount = fields.Monetary(string='Cost Tax Amount', compute="_compute_totals", store=True)
    cost_amount_total = fields.Monetary(string='Cost Total', compute='_compute_totals', store=True)
    cost_post = fields.Boolean(string="Cost Post")
    #
    # sell_currency_id = fields.Many2one('res.currency', string="Company Currency", default=lambda self: self.env.company.currency_id)
    sell_currency_id = fields.Many2one('res.currency', string="Sell Currency", store=True)
    os_sell = fields.Monetary(string="Os Sell", currency_field='currency_id', readonly=True)
    estimated_sell = fields.Monetary(string='Estimated Revenue', currency_field='currency_id')
    local_sell = fields.Monetary(string='Local Cost Sell', currency_field='currency_id', compute="_compute_local_costs",
                                 store=True)
    debtor_id = fields.Many2one('res.partner', string='Debtor',store=True)
    sell_tax_id = fields.Many2many(
        'account.tax',
        'ship_line_charges_tax_rel',
        'charge_id',
        'tax_id',
        string='Sell Tax',compute="_compute_tax_ids")

    # sell_tax_id = fields.Many2many('account.tax', string='Tax')
    sell_tax_amount = fields.Monetary(string='Sell Tax Amount', compute="_compute_totals", store=True)
    sell_amount_total = fields.Monetary(string="Sell Total", compute='_compute_totals', store=True)
    sell_post = fields.Boolean(string='Sell Post')

    amount_cost = fields.Monetary(string='Cost Amount', compute="_compute_totals", store=True)
    amount_sell = fields.Monetary(string='Sell Amount', store=True, compute="_compute_totals")
    amount = fields.Monetary(string='Amount', store=True)
    tax_id = fields.Many2many('account.tax', string='Tax')
    tax_amount = fields.Monetary(string='Tax Amount', compute='_compute_totals', store=True)

    total_cost = fields.Monetary(string='Total Cost', compute='_compute_totals', store=True)
    amount_tax = fields.Monetary(string="Taxes", compute='_compute_totals', store=True)
    amount_untaxed = fields.Monetary(string="Untaxed Amount")
    amount_total = fields.Monetary(string="Total", compute='_compute_totals', store=True)
    narration = fields.Text(string='Narration')

