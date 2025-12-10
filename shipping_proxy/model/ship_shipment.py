from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class ShippingShipment(models.Model):
    _name = "ship.shipment"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Shipment"

    booking_id = fields.Many2one('ship.booking', string='Booking Reference', domain=[('state', '=', 'confirm')])

    company_id = fields.Many2one('res.company', string='Company', readonly=True)
    branch_id = fields.Many2one('res.company', string='Branch', readonly=True)
    department_id = fields.Many2one('ship.department', string='Department', readonly=True)

    name = fields.Char(string="Shipment", required=True, copy=False, readonly=False, default=lambda self: _('New'))
    hbl_date = fields.Date(string='Date', required=True, default=fields.Date.context_today)
    company_id = fields.Many2one('res.company', required=True, default=lambda r: r.env.company)
    mode_id = fields.Many2one('ship.mode', string='Type', related='department_id.mode_id', store=True, readonly=False)
    transport_id = fields.Many2one('ship.transport', string='Transport', related='department_id.transport_id',
                                   store=True, readonly=False)
    type_id = fields.Many2one('ship.type', string='Type', store=True, readonly=False)

    container_id = fields.Many2one('ship.container', string='Container')
    department_id = fields.Many2one('ship.department', string='Department')
    employee_id = fields.Many2one('res.users', string='Sales Person')
    hbl_depdate = fields.Date(string='ETD')
    hbl_arrivaldt = fields.Date(string='ETA')
    hbl_carrier_id = fields.Many2one('ship.carriers', string='Carrier', store="True", readonly=True)
    hbl_vessel_id = fields.Many2one('ship.vessel', string='Vessel')
    hbl_voyage = fields.Char(string='Voyage Number')
    hbl_masterbill = fields.Char(string='Master Bill')
    hbl_housebill = fields.Char(string='House Bill')
    hbl_jobno = fields.Char(string='Job Number')
    inco_id = fields.Many2one('ship.salesterms', string='Inco Terms', store="True")

    hbl_portload_id = fields.Many2one('ship.port', string='Port of Load', store="True",
                                      required=True)
    hbl_portdisch_id = fields.Many2one('ship.port', string='Port of Discharge', store="True",

                                       required=True)
    origin_id = fields.Many2one('ship.port', string="Origin", store="True")
    final_id = fields.Many2one('ship.port', string="Destination", store="True")
    # Booking Details
    country_id = fields.Many2one('res.country')
    state_id = fields.Many2one('res.country.state')
    street = fields.Char(string="Street")
    street2 = fields.Char(string="Street2")
    zip_code = fields.Char(string="Zip Code")
    city = fields.Char(string="City")

    hbl_customer_id = fields.Many2one('res.partner', string='Local Client',
                                      store=True, readonly=False)
    # hbl_customer_id = fields.Many2one('res.partner', string='Customer')
    hbl_customer_street = fields.Char(string='Customer Street', related='hbl_customer_id.street', store=False)
    hbl_customer_street2 = fields.Char(string='Customer Street2', related='hbl_customer_id.street2', store=False)
    hbl_customer_zip_code = fields.Char(string='Customer Zip', related='hbl_customer_id.zip', store=False)
    hbl_customer_city = fields.Char(string='Customer City', related='hbl_customer_id.city', store=False)
    hbl_customer_state_id = fields.Many2one(string='Customer State', related='hbl_customer_id.state_id', store=False)
    hbl_customer_country_id = fields.Many2one(string='Customer Country', related='hbl_customer_id.country_id',
                                              store=False)

    hbl_consigner_id = fields.Many2one('res.partner', string='Consigner',
                                       store=True, readonly=False)
    hbl_consigner_street = fields.Char(string='Consigner Street', related='hbl_consigner_id.street', readonly=False,
                                       store=False)
    hbl_consigner_street2 = fields.Char(string='Consigner Street2', related='hbl_consigner_id.street2', readonly=False,
                                        store=False)
    hbl_consigner_zip_code = fields.Char(string='Consigner Zip', related='hbl_consigner_id.zip', readonly=False,
                                         store=False)
    hbl_consigner_city = fields.Char(string='Consigner City', related='hbl_consigner_id.city', readonly=False,
                                     store=False)
    hbl_consigner_state_id = fields.Many2one("res.country.state", string='Consigner State',
                                             related='hbl_consigner_id.state_id', readonly=False, store=False)
    hbl_consigner_country_id = fields.Many2one('res.country', string='Consigner Country',
                                               related='hbl_consigner_id.country_id', readonly=False, store=False)

    hbl_consignee_id = fields.Many2one('res.partner', string='Consginee',
                                       store=True, readonly=False)
    hbl_consignee_street = fields.Char(string='Consignee Street', related='hbl_consignee_id.street', readonly=False,
                                       store=False)
    hbl_consignee_street2 = fields.Char(string='Consignee Street2', related='hbl_consignee_id.street2', readonly=False,
                                        store=False)
    hbl_consignee_zip_code = fields.Char(string='Consignee Zip', related='hbl_consignee_id.zip', readonly=False,
                                         store=False)
    hbl_consignee_city = fields.Char(string='Consignee City', related='hbl_consignee_id.city', readonly=False,
                                     store=False)
    hbl_consignee_state_id = fields.Many2one("res.country.state", string='Consignee State',
                                             related='hbl_consignee_id.state_id', readonly=False, store=False)
    hbl_consignee_country_id = fields.Many2one('res.country', string='Consignee Country',
                                               related='hbl_consignee_id.country_id', readonly=False, store=False)

    hbl_interconsig_id = fields.Many2one('res.partner', string='Intermediate Consignee')
    hbl_interconsig_street = fields.Char(string='Inter Consignee Street', related='hbl_interconsig_id.street',
                                         readonly=False, store=False)
    hbl_interconsig_street2 = fields.Char(string='Inter Consignee Street2', related='hbl_interconsig_id.street2',
                                          readonly=False, store=False)
    hbl_interconsig_zip_code = fields.Char(string='Inter Consignee zip', related='hbl_interconsig_id.zip',
                                           readonly=False, store=False)
    hbl_interconsig_city = fields.Char(string='Inter Consignee City', related='hbl_interconsig_id.city', readonly=False,
                                       store=False)
    hbl_interconsig_state_id = fields.Many2one("res.country.state", string='Inter Consignee State',
                                               related='hbl_interconsig_id.state_id', readonly=False, store=False)
    hbl_interconsig_country_id = fields.Many2one('res.country', string='Inter Consignee Country',
                                                 related='hbl_interconsig_id.country_id', readonly=False, store=False)

    hbl_notify_id = fields.Many2one('res.partner', string='Notify Agent')
    hbl_notify_street = fields.Char(string='Notify Agent Street', related='hbl_notify_id.street', readonly=False,
                                    store=False)
    hbl_notify_street2 = fields.Char(string='Notify Agent Street2', related='hbl_notify_id.street2', readonly=False,
                                     store=False)
    hbl_notify_zip_code = fields.Char(string='Notify Agent Zip', related='hbl_notify_id.zip', readonly=False,
                                      store=False)
    hbl_notify_city = fields.Char(string='Notify Agent City', related='hbl_notify_id.city', readonly=False, store=False)
    hbl_notify_state_id = fields.Many2one("res.country.state", string='Notify Agent State',
                                          related='hbl_notify_id.state_id', readonly=False, store=False)
    hbl_notify_country_id = fields.Many2one('res.country', string='Notify Agent Country',
                                            related='hbl_notify_id.country_id', readonly=False, store=False)

    hbl_loadagent_id = fields.Many2one('res.partner', string='Loading Agent')
    hbl_loadagent_street = fields.Char(string='Loading Agent Street', related='hbl_loadagent_id.street', readonly=False,
                                       store=False)
    hbl_loadagent_street2 = fields.Char(string='Loading Agent Street2', related='hbl_loadagent_id.street2',
                                        readonly=False, store=False)
    hbl_loadagent_zip_code = fields.Char(string='Loading Agent Zip', related='hbl_loadagent_id.zip', readonly=False,
                                         store=False)
    hbl_loadagent_city = fields.Char(string='Loading Agent City', related='hbl_loadagent_id.city', readonly=False,
                                     store=False)
    hbl_loadagent_state_id = fields.Many2one("res.country.state", string='Loading Agent State',
                                             related='hbl_loadagent_id.state_id', readonly=False, store=False)
    hbl_loadagent_country_id = fields.Many2one('res.country', string='Loading Agent Country',
                                               related='hbl_loadagent_id.country_id', readonly=False, store=False)

    hbl_destagent_id = fields.Many2one('res.partner', string='Destination Agent')
    hbl_destagent_street = fields.Char(string='Destination Agent Street', related='hbl_destagent_id.street',
                                       readonly=False, store=False)
    hbl_destagent_street2 = fields.Char(string='Destination Agent Street2', related='hbl_destagent_id.street2',
                                        readonly=False, store=False)
    hbl_destagent_zip_code = fields.Char(string='Destination Agent Zip', related='hbl_destagent_id.zip', readonly=False,
                                         store=False)
    hbl_destagent_city = fields.Char(string='Destination Agent City', related='hbl_destagent_id.city', readonly=False,
                                     store=False)
    hbl_destagent_state_id = fields.Many2one("res.country.state", string='Destination Agent State',
                                             related='hbl_destagent_id.state_id', readonly=False)
    hbl_destagent_country_id = fields.Many2one('res.country', string='Destination Agent Country',
                                               related='hbl_destagent_id.country_id', readonly=False)

    hbl_rcptplace_id = fields.Many2one('ship.location', string='Receipt Place')
    hbl_delvplace_id = fields.Many2one('ship.location', string='Delivery Place')
    hbl_pick_addr = fields.Many2one('ship.location', string='Pick up Address')
    hbl_deliv_addr = fields.Many2one('ship.location', string='Delivery Address')
    hbl_pick_cfs = fields.Char(string='Pick up CFS')
    hbl_delv_cfs = fields.Char(string='Delivery CFS')
    hbl_pick_agent_id = fields.Many2one('res.partner', string='Pick Agent')
    hbl_deliv_agent_id = fields.Many2one('res.partner', string='Delivery Agent')

    # Custom Details
    hbl_boepaid = fields.Boolean(string='BOE/IGM Paid')
    hbl_boedate = fields.Date(string='BOE/IGM Date')
    hbl_boeno = fields.Char(string='BOE/ OHM Number')
    hbl_boedays = fields.Integer(string='No of days')
    hbl_boeamt = fields.Float(string='Amount')
    hbl_boerefund = fields.Boolean(string='BOE/IGM Refunded')
    hbl_boerefdate = fields.Date(string='Refund Date')
    hbl_refuamt = fields.Float(string='Refund Amount')
    hbl_custreldate = fields.Date(string='Custom Release Date')
    hbl_custexamdate = fields.Date(string='Custom Exam Date')
    hbl_custexamreldate = fields.Date(string='Custom Exam Release Date')
    hbl_linereldate = fields.Date(string='Line  Release Date')
    hbl_examtypedate = fields.Date(string='Exam  Date')
    hbl_godate = fields.Date(string='Go Date')
    ship_date = fields.Date(string='Ship Date')
    hbl_client_wt = fields.Float(string='Client Wt.')
    hbl_client_vol = fields.Float(string='Client Vol')
    hbl_client_chargable = fields.Float(string='Client Chargable')
    hbl_mark = fields.Text(string='Marks$ Numbs')
    hbl_desc = fields.Text(string='Description')
    hbl_addterms = fields.Text(string='Additional Terms')
    hbl_carrier_wt = fields.Float(string='Carrier Wt.')
    hbl_carrier_vol = fields.Float(string='Carrier Vol')
    hbl_carrier_chargable = fields.Float(string='Carrier Chargable')

    hbl_weight = fields.Float(string='Weight')
    hbl_wtuom = fields.Selection([
        ('kgm', 'KGM'), ], string='Weight Uom', default='kgm')
    hbl_volume  = fields.Float(string='Volune')
    hbl_voluom = fields.Selection([
        ('m3', 'M3'), ], string='Vol Weight Uom', default='m3')
    hbl_chrgble  = fields.Float(string='Chargable')

    hbl_wv = fields.Float(string='WV')

    hbl_pack =fields.Float(string='Packs')
    hbl_pktype = fields.Selection([
        ('m3', 'M3'), ], string='Vol Weight Uom', default='m3')
    hbl_inner = fields.Float(string='Inners')
    hbl_inntype = fields.Selection([
        ('m3', 'M3'), ], string='Vol Weight Uom', default='m3')

    currency_id = fields.Many2one('res.currency', 'Çurrency', required=True,
                                  default=lambda self: self.env.company.currency_id)

    amount_untaxed = fields.Monetary(string="Untaxed Amount")
    amount_tax = fields.Monetary(string="Taxes", )
    amount_total = fields.Monetary(string="Total")

    income = fields.Monetary(string="Income", store=True, compute='_compute_income_expense')
    expense = fields.Monetary(string="Expense", store=True, compute='_compute_income_expense')
    profit_loss = fields.Monetary(string='Profit/Loss', store=True, compute='_compute_profit_loss')
    profit_loss_percentage = fields.Float(string='Profit/Loss %', store=True, compute='_compute_profit_loss')

    hbl_charges_ids = fields.One2many('ship.shipment.charges', 'hbl_charges_id', string='Shipment Charges')
    hbl_commodity_ids = fields.One2many('ship.shipment.commodity', 'hbl_commodity_id', string='Commodity Details')
    # hbl_edoc_ids = fields.One2many('ship.shipment.edocs', 'hbl_edocs_id', string='E Documents')
    shipment_job_ids = fields.Many2many('ship.joborder', 'ship_job_id', string='Consol Details')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirmed'),
        ('invoice', 'Invoiced'),
        ('cancel', 'Cancel'),
        # Add more states as needed
    ], string='Status', default='draft', clickable=True)

    tax_totals = fields.Binary(compute='_compute_tax_totals', exportable=False)

    # Commodity Details
    hbl_recvtdt = fields.Date(string='Receiving Date')
    hbl_movtype = fields.Char(string='Movement Type')
    hbl_packdesc = fields.Text(string='Goods General Description')
    hbl_handling = fields.Text(string='Handling Information')

    hbliss_date = fields.Date(string='Issue Date')
    orignal_ct = fields.Integer(string='Originals')
    copy_ct = fields.Integer(string='Copy Bills')
    gross_value = fields.Float(string='Gross Value')
    insur_value = fields.Float(string='Insurance Value')

    hbl_reltype = fields.Selection([
        ('EBL', 'Express Bill of Lading'),
        ('CAD', 'Cash Against Document'),
        # Add more states as needed
    ], string='Release Type', default='EBL', clickable=True)

    hbl_chrgapply = fields.Selection([
        ('NON', 'No Charges Showing'),
        ('SHW', 'Show Collect Charges'),
        # Add more states as needed
    ], string='Charges Apply', default='SHW', clickable=True)

    invoice_count = fields.Integer(compute='compute_invoice')
    purchase_count = fields.Integer(compute='compute_purchase')

    company_desc = fields.Char(string='Company ', compute="_compute_company_description", store=True)
    job_attached = fields.Boolean(string='Job Attached', default=False)
    jobstatus_id = fields.Many2one('ship.jobstatus', string='Job Status')
    jobstatus_code = fields.Char(related='jobstatus_id.code', store=True)
    hold_reason = fields.Char(string='Hold reason')
    servicelevel_id = fields.Many2one('ship.servicelevel', string='Service Level')
    can_change_state = fields.Boolean(string="Can Change State", groups="shipping.group_shipping_admin",
                                      default="False")
    joborder_id = fields.Many2one('ship.joborder',string='Job order')


class ShipmentCharges(models.Model):
    _name = "ship.shipment.charges"
    _description = "Shipment Charges"

    booking_id = fields.Many2one('ship.booking')
    shipment_id = fields.Many2one('ship.shipment')

    selected = fields.Boolean(string=' ')
    charge_id = fields.Many2one('product.product', string='Charge', required=True)
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id)
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
    cost_post = fields.Boolean(string="Cost Post", default=False)
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
    sell_post = fields.Boolean(string='Sell Post', store=True, default=False)

    amount_cost = fields.Monetary(string='Cost Amount', compute="_compute_totals", store=True)
    amount_sell = fields.Monetary(string='Sell Amount', compute="_compute_totals", store=True)
    amount = fields.Monetary(string='Amount', store=True)
    tax_id = fields.Many2many('account.tax', string='Tax')
    tax_amount = fields.Monetary(string='Tax Amount', compute='_compute_totals', store=True)

    total_cost = fields.Monetary(string='Total Cost', compute='_compute_totals', store=True)
    amount_tax = fields.Monetary(string="Taxes", compute='_compute_totals', store=True)
    amount_untaxed = fields.Monetary(string="Untaxed Amount")
    amount_total = fields.Monetary(string="Total", compute='_compute_totals', store=True)
    narration = fields.Text(string='Narration')

    hbl_charges_id = fields.Many2one('ship.shipment', string='Charge Details')
    ship_state = fields.Selection(related='hbl_charges_id.state', string="State", store=True)
    invoiced = fields.Boolean(string='Invoiced', default=False)
    purchased = fields.Boolean(string='Purchased', default=False)

class ShipShipcommodity(models.Model):
    _name = "ship.shipment.commodity"
    _description = "Shipment Commodity Details"

    # Container Details

    hbl_contno = fields.Char(string='Container No')
    hbl_sealno = fields.Char(string='Seal No')
    hbl_conttype_id = fields.Many2one('ship.containertype', string='Continer Type', store=True)
    hbl_delvtype = fields.Selection([
        ('gen', 'GEN'),
        ('dgr', 'DGR'),
        ('oog', 'OOG'),

    ], string='Delivery Type', default='gen')
    hbl_fe = fields.Char(string='F/E')

    # Commodity Details

    hbl_packtype_id = fields.Many2one('ship.packagetype', string='Package Type', store=True)
    hbl_pieces = fields.Integer(string='Pieces')
    hbl_commod_id = fields.Many2one('ship.commodity', string='Çommodity', store=True)
    hbl_hscode = fields.Char(string='HS Code')
    hbl_marksno = fields.Char(string='Marks & Numbers')
    hbl_danger = fields.Boolean(string='Dangerous Goods')
    hbl_imdgno = fields.Char(string='ÍMDG No')
    hbl_umno = fields.Char(string='ÚM No')
    hbl_length = fields.Float(string='Length', related='hbl_conttype_id.length', store=True)
    hbl_length_id = fields.Selection([
        ('cent', 'Centimeter'),
        ('mtr', 'Meter'), ], string='Length Uom', default='mtr')
    hbl_height = fields.Float(string='Height', related='hbl_conttype_id.height', store=True)
    hbl_height_id = fields.Selection([
        ('cent', 'Centimeter'),
        ('mtr', 'Meter'), ], string='Height Uom', default='mtr')
    hbl_width = fields.Float(string='Width', related='hbl_conttype_id.width', store=True)
    hbl_width_id = fields.Selection([
        ('cent', 'Centimeter'),
        ('mtr', 'Meter'), ], string='Width Uom', default='mtr')
    hbl_weight = fields.Float(string='Weight', related='hbl_conttype_id.weight', store=True)
    hbl_weight_id = fields.Selection([
        ('kgm', 'KGM'), ], string='Weight Uom', default='kgm')
    hbl_volume = fields.Float(string='Volume', related='hbl_conttype_id.volume', store=True)

    hbl_volume_id = fields.Selection([
        ('m3', 'M3'), ], string='Vol Weight Uom', default='m3')

    hbl_commodity_id = fields.Many2one('ship.shipment', string='Commodity Details', store=True)


class AccountMove(models.Model):
    _inherit = 'account.move'

    shipment_number = fields.Char(string="Shipment Number")
