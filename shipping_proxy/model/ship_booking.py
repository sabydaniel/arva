from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class ShippingBooking(models.Model):
    _name = "ship.booking"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Booking"

    quote_id = fields.Many2one('ship.quote', string='Quote No', domain=[('state', '=', 'confirm')], store=True)
    name = fields.Char(string="Booking Number", required=True, copy=False, readonly=False,
                       default=lambda self: _('New'))
    # shipline_id = fields.Many2one('ship.carriers',
    #                               string='Carrier Name')
    selected = fields.Boolean('Selected')

    company_id = fields.Many2one('res.company', string='Company', related='quote_id.company_id', readonly=True)
    branch_id = fields.Many2one('res.company', string='Branch', related='quote_id.branch_id', readonly=True)
    department_id = fields.Many2one('ship.department', string='Department', related='quote_id.department_id',
                                    readonly=True)
    container_id = fields.Many2one('ship.container', string='Container',related='quote_id.container_id', store=True)
    # branch_id = fields.Integer(default='1')
    service_id = fields.Many2one('ship.servicelevel', string='Service Level')
    bk_date = fields.Date(string='Booked Date')
    bk_etd = fields.Date(string='ETD')
    bk_eta = fields.Date(string='ETA')
    est_pick = fields.Date(string='Est Pickup')
    est_delv = fields.Date(string='Est Delivery')
    bk_marksno = fields.Text(string='Marks & Numbers')
    bk_loadport_id = fields.Many2one('ship.unlocode', string='Load Location')
    bk_dischaport_id = fields.Many2one('ship.unlocode', string='Discharge Location')
    bk_estdepart_dt = fields.Date(string='Est. Departure Date')
    bk_estarrival_dt = fields.Date(string='Est. Arrival Date')
    bk_flgtvessel_id = fields.Many2one('ship.vessel', string='Flight/Vessel Details')

    bk_pickaddr_id = fields.Many2one('res.partner', string='Pick up Address')
    pick_street = fields.Char(related='bk_pickaddr_id.street', string='Pick up Street', store=False)
    pick_street2 = fields.Char(related='bk_pickaddr_id.street2', string='Pick up Street2', store=False)
    pick_zip_code = fields.Char(related='bk_pickaddr_id.zip', string='Pick up ZIP Code', store=False)
    pick_city = fields.Char(related='bk_pickaddr_id.city', string='Pick upCity', store=False)
    pick_state_id = fields.Many2one(related='bk_pickaddr_id.state_id', string="Pick up State", store=False)
    pick_country_id = fields.Many2one(related='bk_pickaddr_id.country_id', string="Pick up Country", store=False)

    bk_delivaddr_id= fields.Many2one('res.partner', string='Delivery Address')
    deliv_street = fields.Char(related='bk_delivaddr_id.street', string='Delivery Street', store=False)
    deliv_street2 = fields.Char(related='bk_delivaddr_id.street2', string='Delivery Street2', store=False)
    deliv_zip_code = fields.Char(related='bk_delivaddr_id.zip', string='Delivery ZIP Code', store=False)
    deliv_city = fields.Char(related='bk_delivaddr_id.city', string='Delivery City', store=False)
    deliv_state_id = fields.Many2one(related='bk_delivaddr_id.state_id', string="Delivery State", store=False)
    deliv_country_id = fields.Many2one(related='bk_pickaddr_id.country_id', string="Delivery Country", store=False)

    bk_pick_cfs = fields.Char(string='Pick up CFS')
    bk_delv_cfs = fields.Char(string='Delivery CFS')

    bk_pick_agent_id = fields.Many2one('res.partner', string='Pickup Agent')
    pick_agent_street = fields.Char(related='bk_pick_agent_id.street', string='Pickup Agent Street', store=False)
    pick_agent_street2 = fields.Char(related='bk_pick_agent_id.street2', string='Pickup Agent Street2', store=False)
    pick_agent_zip_code = fields.Char(related='bk_pick_agent_id.zip', string='Pickup Agent ZIP Code', store=False)
    pick_agent_city = fields.Char(related='bk_pick_agent_id.city', string='Pickup Agent City', store=False)
    pick_agent_state_id = fields.Many2one(related='bk_pick_agent_id.state_id', string="Pickup Agent State", store=False)
    pick_agent_country_id = fields.Many2one(related='bk_pick_agent_id.country_id', string="Pickup Agent Country", store=False)

    bk_deliv_agent_id = fields.Many2one('res.partner', string='Delivery Agent')
    deliv_agent_street = fields.Char(related='bk_pickaddr_id.street', string='Delivery Agent Street', store=False)
    deliv_agent_street2 = fields.Char(related='bk_pickaddr_id.street2', string='Delivery Agent Street2', store=False)
    deliv_agent_zip_code = fields.Char(related='bk_pickaddr_id.zip', string='Delivery Agent ZIP Code', store=False)
    deliv_agent_city = fields.Char(related='bk_pickaddr_id.city', string='Delivery Agent City', store=False)
    deliv_agent_state_id = fields.Many2one(related='bk_pickaddr_id.state_id', string="Delivery AgentState", store=False)
    deliv_agent_country_id = fields.Many2one(related='bk_pickaddr_id.country_id', string="Delivery Agent Country", store=False)
    bk_hbl_number = fields.Char(string='HBL Number')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirmed'),
        ('ship', 'Shipment'),
        ('cancel', 'Cancel'),
        # Add more states as needed
    ], string='Status', default='draft')

    country_id = fields.Many2one('res.country')
    state_id = fields.Many2one('res.country.state')
    street = fields.Char(string="Street")
    street2 = fields.Char(string="Street2")
    zip_code = fields.Char(string="Zip Code")
    city = fields.Char(string="City")

    client_id = fields.Many2one('res.partner', string='Client', required=True, domain=[('customer_rank', '>', 0)],
                                related='quote_id.client_id', store=True)

    client_street = fields.Char(related='client_id.street', string='Client Street', store=False)
    client_street2 = fields.Char(related='client_id.street2', string='Client Street2', store=False)
    client_zip_code = fields.Char(related='client_id.zip', string='Client ZIP Code', store=False)
    client_city = fields.Char(related='client_id.city', string='Client City', store=False)
    client_state_id = fields.Many2one(related='client_id.state_id', string="Client State", store=False)
    client_country_id = fields.Many2one(related='client_id.country_id', string="Client Country", store=False)

    consignor_id = fields.Many2one('res.partner', string='Consigner', required=True,
                                   domain="[('consigner', '=', True)]", related='quote_id.client_id', store=True)

    consignor_street = fields.Char(related='consignor_id.street', string='Consigner Street', store=False)
    consignor_street2 = fields.Char(related='consignor_id.street2', string='Consigner Street2', store=False)
    consignor_zip_code = fields.Char(related='consignor_id.zip', string='Consigner ZIP Code', store=False)
    consignor_city = fields.Char(related='consignor_id.city', string='Consigner City', store=False)
    consignor_state_id = fields.Many2one(related='consignor_id.state_id', string="Consigner State", store=False)
    consignor_country_id = fields.Many2one(related='consignor_id.country_id', string="Consigner Country", store=False)

    consignee_id = fields.Many2one('res.partner', string='Consignee', required=True,
                                   domain="[('consignee', '=', True)]", store=True)
    consignee_street = fields.Char(related='consignee_id.street', string='Consignee Street', store=False)
    consignee_street2 = fields.Char(related='consignee_id.street2', string='Consignee Street2', store=False)
    consignee_zip_code = fields.Char(related='consignee_id.city', string='Consignee ZIP Code', store=False)
    consignee_city = fields.Char(related='consignee_id.city', string='Consignee City', store=False)
    consignee_state_id = fields.Many2one(related='consignee_id.state_id', string="Consignee State", store=False)
    consignee_country_id = fields.Many2one(related='consignee_id.country_id', string="Consignee Country", store=False)

    # quote_id = fields.Char(string = 'Quote Reference', related='quote_id.id')
    mode_id = fields.Many2one('ship.mode', string='Type', related='department_id.mode_id', store=True, readonly=True)
    transport_id = fields.Many2one('ship.transport', string='Transport', related='department_id.transport_id',
                                   readonly=True, store=True)
    mode_id = fields.Many2one('ship.mode', string='Mode', related='quote_id.mode_id', store=True)
    # mode = fields.Char(related="quote_id.mode_id.code")
    quote_date = fields.Date(string='Date', related='quote_id.quote_date')
    quote_startdt = fields.Date(string='Start Date', related='quote_id.quote_date')
    qutoe_enddt = fields.Date(string='Validity Till', related='quote_id.qutoe_enddt')

    employee_id = fields.Many2one('res.users', string='Sales Person', related='quote_id.employee_id', store=True)
    agent_id = fields.Many2one('res.partner', string='Agent', related='quote_id.agent_id', store=True)
    code = fields.Many2one('ship.department', string='Department Code', related='quote_id.code', store=True)
    inco_id = fields.Many2one('ship.salesterms', string='Inco Terms', related='quote_id.inco_id', store=True)
    add_terms = fields.Char(string='Ädd. Terms', related='quote_id.add_terms')
    orgin_id = fields.Many2one('ship.port', string='Port of Loading', related='quote_id.orgin_id', store=True,
                               required=True)
    dest_id = fields.Many2one('ship.port', string="Port of Discharge", related='quote_id.dest_id', store=True,
                              required=True)
    final_id = fields.Many2one('ship.port', string="Final Destination", related='quote_id.final_id', store=True)
    via_id = fields.Many2one('ship.port', string='Via', related='quote_id.via_id')
    transit_time = fields.Integer(string='Transit Time', related='quote_id.transit_time')
    package_id = fields.Many2many('ship.packagetype', string='Package Type', store=True)
    quote_weight = fields.Float(string='Weight', related='quote_id.quote_weight')
    weight_uom = fields.Selection([
        ('g', 'Gram'),
        ('kg', 'Kilogram')
    ], string=' Weight Unit', default='kg')
    quote_volume = fields.Float(string='Volume', related='quote_id.quote_volume')
    volume_uom = fields.Selection([
        ('m3', 'CM3'),
    ], string='Volume Unit', default='m3')
    quote_chargable = fields.Float(string='Chargable', related='quote_id.quote_chargable')
    goods_value = fields.Float(string='Goods Value', related='quote_id.goods_value')
    insur_value = fields.Float(string='Insured Value', related='quote_id.insur_value')
    commodity_id = fields.Many2one('ship.commodity', string='Commodity', related='quote_id.commodity_id')
    picdrop = fields.Boolean(string='Pick / Drop', related='quote_id.picdrop')
    country_origin = fields.Many2one('res.country', string='Country of origin', related='quote_id.country_origin')
    dg_applicable = fields.Boolean(string="DG", related='quote_id.dg_applicable')
    dg_class = fields.Char(string='Classification', related='quote_id.dg_class')
    delivery_id = fields.Many2one(string="Delivery Mode", related='quote_id.delivery_id')

    currency_id = fields.Many2one('res.currency', 'Çurrency', required=True,
                                  default=lambda self: self.env.company.currency_id, store=True)

    income = fields.Monetary(string='Income', store=True, compute='_compute_income_expense')
    expense = fields.Monetary(string='Expense', store=True, compute='_compute_income_expense')
    profit_loss = fields.Monetary(string='Profit/Loss', store=True, compute='_compute_profit_loss')
    profit_loss_percentage = fields.Float(string='Profit/Loss %', store=True, compute='_compute_profit_loss')

    book_cargo_ids = fields.One2many('ship.book.cargo', 'book_cargo_id', string='Booking Details')
    # bookshpline_ids = fields.One2many('ship.quote.line', compute="_compute_selected_ship_quote_line")
    booklinecharge_ids = fields.One2many('ship.book.line.charges', 'line_charge_id', string='Booking Charges')

    carrier_id = fields.Many2one('ship.carriers', string='Carrier', compute='get_carrier_id', store=True)

    company_desc = fields.Char(string='Company ', compute="_compute_company_description", store=True)
    consol_count = fields.Integer(compute='compute_consol')

class ShipBookLineCharges(models.Model):
    _name = "ship.book.line.charges"
    _description = "Booking Line Charges"

    ship_quote_id = fields.Many2one('ship.quote')
    line_charge_id = fields.Many2one('ship.booking')

    charge_id = fields.Many2one('product.product', string='Charge', required=True)
    currency_id = fields.Many2one(
        related='ship_quote_id.currency_id',
        depends=['ship_quote_id.currency_id'],
        store=True, precompute=True, )

    company_currency_id = fields.Many2one('res.currency', string="Company Currency",
                                          default=lambda self: self.env.company.currency_id)
    cost_currency_id = fields.Many2one('res.currency', string="Cost Currency", store=True)
    os_cost = fields.Monetary(string='OS Cost', currency_field='currency_id', readonly=True)
    estimated_cost = fields.Monetary(string='Estimated Cost', currency_field='currency_id')
    local_cost = fields.Monetary(string='Local Cost', currency_field='currency_id', compute="_compute_local_costs",
                                 store=True)
    creditor_id = fields.Many2one('res.partner', string="Creditor", store=True)

    cost_tax_id = fields.Many2many(
        'account.tax',
        'ship_line_charges_tax_rel',
        'charge_id',
        'tax_id',
        string='Cost Tax', compute="_compute_tax_ids")
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
    debtor_id = fields.Many2one('res.partner', string='Debtor', store=True)
    sell_tax_id = fields.Many2many(
        'account.tax',
        'ship_line_charges_tax_rel',
        'charge_id',
        'tax_id',
        string='Sell Tax', compute="_compute_tax_ids")

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


class ShipBookcargo(models.Model):
    _name = "ship.book.cargo"
    _description = "Booking Cargo Details"

    # Container Details
    quote_id = fields.Many2one('ship.quote')

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
    crg_length = fields.Float(string='Lenght')
    crg_length_id = fields.Selection([
        ('cent', 'Centimeter'),
        ('mtr', 'Meter'), ], string='Length Uom')
    crg_height = fields.Float(string='Height')
    crg_height_id = fields.Selection([
        ('cent', 'Centimeter'),
        ('mtr', 'Meter'), ], string='Height Uom')
    crg_width = fields.Float(string='Width')
    crg_width_id = fields.Selection([
        ('cent', 'Centimeter'),
        ('mtr', 'Meter'), ], string='Width Uom')
    crg_weight = fields.Float(string='Weight')
    crg_weight_id = fields.Selection([
        ('kgm', 'KGM'), ], string='Weight Uom', default='kgm')
    crg_volume = fields.Float(string='Volume')
    crg_volume_id = fields.Selection([
        ('m3', 'M3'), ], string='Vol Weight Uom', default='m3')

    book_cargo_id = fields.Many2one('ship.booking', string='Cargo Details')
