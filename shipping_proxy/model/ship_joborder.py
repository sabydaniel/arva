from odoo import api, fields, models, _


class ShippingJoborder(models.Model):
    _name = "ship.joborder"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Job Order"

    shipment_id = fields.Many2one('ship.shipment')
    booking_id = fields.Many2one('ship.booking', string='Booking Reference')
    name = fields.Char(string="Consol No", required=True, copy=False, readonly=False, default=lambda self: _('New'))
    company_id = fields.Many2one('res.company', string='Company', readonly=True)
    branch_id = fields.Many2one('res.company', string='Branch', readonly=True)
    department_id = fields.Many2one('ship.department', string='Department', readonly=True)

    job_date = fields.Date(string='Date', default=fields.Date.context_today)
    mode_id = fields.Many2one('ship.mode', string='Mode')
    consoletype_id = fields.Many2one('ship.consoletype', string='Type')
    transport_id = fields.Many2one('ship.transport', string='Transport')
    container_id = fields.Many2one('ship.container', string='Container')
    domestic = fields.Boolean(string='Domestic')
    type_id = fields.Many2one('ship.type', string='Mode')
    code = fields.Char(related='department_id.code')
    job_depdate = fields.Date(string='Departure Date')
    job_arrivaldt = fields.Date(string='Arrival Date')
    job_atd = fields.Date(string='Actual Departure Date')
    job_ata = fields.Date(string='Actual Arrival Date')
    # job_type = fields.Selection([('export', 'Export'), ('import', 'Import')], string='Type')                             )
    job_carrier_id = fields.Many2one('ship.carriers', string='Carrier')
    job_vessel_id = fields.Many2one('ship.vessel', string='Vessel')
    job_voyage = fields.Char(string='Voyage Number')
    job_masterbill = fields.Char(string='Master Bill')
    job_refjobno = fields.Char(string='Reference Number')
    job_hblno = fields.Char(string='HBL Number')
    job_mblno = fields.Char(string='Ref MBL/MAWBNo')
    job_linecode = fields.Char(string='Line Code')
    job_boeno = fields.Char(string='BOE Code')
    job_portload_id = fields.Many2one('ship.port', string='Port of Load')
    job_portdisch_id = fields.Many2one('ship.port', string='Port of Discharge')
    origin_id = fields.Many2one('ship.port', string='Origin')
    final_id = fields.Many2one('ship.port', string='Destination')

    # Booking Details
    party_type = fields.Selection([
        ('customer', 'Customer'),
        ('agent', 'Forwarding Agent'),

    ], string='Party Type', default='customer')

    country_id = fields.Many2one('res.country')
    state_id = fields.Many2one('res.country.state')
    street = fields.Char(string="Street")
    street2 = fields.Char(string="Street2")
    zip_code = fields.Char(string="Zip Code")
    city = fields.Char(string="City")

    job_loadagent_id = fields.Many2one('res.partner', string='Sending Agent')
    job_loadagent_street = fields.Char(string='Loading Agent Street', related='job_loadagent_id.street', store=False)
    job_loadagent_street2 = fields.Char(string='Loading Agent Street2', related='job_loadagent_id.street2', store=False)
    job_loadagent_zip_code = fields.Char(string='Loading Agent Zip', related='job_loadagent_id.zip', store=False)
    job_loadagent_city = fields.Char(string='Loading Agent City', related='job_loadagent_id.city', store=False)
    job_loadagent_state_id = fields.Many2one("res.country.state", string='Loading Agent State',
                                             related='job_loadagent_id.state_id', store=False)
    job_loadagent_country_id = fields.Many2one('res.country', string='Loading Agent Country',
                                               related='job_loadagent_id.country_id', store=False)

    job_destagent_id = fields.Many2one('res.partner', string='Receiving Agent')
    job_destagent_street = fields.Char(string='Destination Agent Street', related='job_destagent_id.street',
                                       store=False)
    job_destagent_street2 = fields.Char(string='Destination Agent Street2', related='job_destagent_id.street2',
                                        store=False)
    job_destagent_zip_code = fields.Char(string='Destination Agent Zip', related='job_destagent_id.zip', store=False)
    job_destagent_city = fields.Char(string='Destination Agent City', related='job_destagent_id.city', store=False)
    job_destagent_state_id = fields.Many2one("res.country.state", string='Destination Agent State',
                                             related='job_destagent_id.state_id', store=False)
    job_destagent_country_id = fields.Many2one('res.country', string='Destination Agent Country',
                                               related='job_destagent_id.country_id', store=False)

    job_rcptplace_id = fields.Many2one('ship.location', string='Receipt Place')
    job_delvplace_id = fields.Many2one('ship.location', string='Delivery Place')
    job_pick_addr = fields.Many2one('ship.location', string='Pick up Address')
    job_deliv_addr = fields.Many2one('ship.location', string='Delivery Address')
    job_pick_cfs = fields.Char(string='Pick up CFS')
    job_delv_cfs = fields.Char(string='Delivery CFS')
    job_pick_agent_id = fields.Many2one('res.partner', string='Pickup Agent')
    job_deliv_agent_id = fields.Many2one('res.partner', string='Delivery Agent')

    # Custom Details
    job_boepaid = fields.Boolean(string='BOE/IGM Paid')
    job_boedate = fields.Date(string='BOE/IGM Date')
    job_boeno = fields.Char(string='BOE/ OHM Number')
    job_boedays = fields.Integer(string='No of days')
    job_boeamt = fields.Float(string='Amount')
    job_boerefund = fields.Boolean(string='BOE/IGM Refunded')
    job_boerefdate = fields.Date(string='Refund Date')
    job_refuamt = fields.Float(string=' Refund Amount')
    job_custreldate = fields.Date(string='Custom Release Date')
    job_custexamdate = fields.Date(string='Custom Exam Date')
    job_custexamreldate = fields.Date(string='Custom Exam Release Date')
    job_linereldate = fields.Date(string='Line  Release Date')
    job_examtypedate = fields.Date(string='Exam  Date')
    job_godate = fields.Date(string='Go Date')

    shipment_ids = fields.One2many('ship.shipment', 'joborder_id', string='Shipments')
    job_commodity_ids = fields.Many2many('ship.job.commodity', string='Shipment Commodity Details')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirmed'),
        ('close', 'Closed'),
        ('cancel', 'Cancelled'),
        # Add more states as needed
    ], string='Status', default='draft')

    # Commodity Details

    company_desc = fields.Char(string='Company ', compute="_compute_company_description", store=True)

    job_recvtdt = fields.Date(string='Reciveing Date')
    job_packdesc = fields.Text(string='Goods Description')
    shipment_count = fields.Integer(string='Shipments', compute='compute_shipments')
    first_shipment = fields.Char()


class ShipJobcommodity(models.Model):
    _name = "ship.job.commodity"
    _description = "Job Commodity Details"

    job_packtype_id = fields.Many2one('ship.packagetype', string='Package Type')
    job_pieces = fields.Integer(string='Pieces')
    job_commod_id = fields.Many2one('ship.commodity', string='Çommodity')
    job_hscode = fields.Char(string='HS Code')
    job_marksno = fields.Char(string='Marks & Numbers')
    job_danger = fields.Boolean(string='Dangerous Goods')
    job_imdgno = fields.Char(string='ÍMDG No')
    job_umno = fields.Char(string='ÚM No')
    job_length = fields.Float(string='Lenght')
    job_length_id = fields.Selection([
        ('cent', 'Centimeter'),
        ('mtr', 'Meter'), ], string='Length Uom')
    job_height = fields.Float(string='Height')
    job_height_id = fields.Selection([
        ('cent', 'Centimeter'),
        ('mtr', 'Meter'), ], string='Height Uom')
    job_width = fields.Float(string='Width')
    job_width_id = fields.Selection([
        ('cent', 'Centimeter'),
        ('mtr', 'Meter'), ], string='Width Uom')
    job_weight = fields.Float(string='Weight')
    job_weight_id = fields.Selection([
        ('kgm', 'KGM'), ], string='Weight Uom')
    job_volume = fields.Float(string='Volume')
    job_volume_id = fields.Selection([
        ('m3', 'CBM'), ], string='Volume Uom')

    job_contno = fields.Char(string='Container No')
    job_sealno = fields.Char(string='Seal No')
    job_conttype_id = fields.Many2one('ship.containertype', string='Continer Type')
    job_delvtype = fields.Selection([
        ('gen', 'GEN'),
        ('dgr', 'DGR'),
        ('oog', 'OOG'),

    ], string='Delivery Type', default='GEN')
    job_fe = fields.Char(string='F/E')
    job_tare_wt = fields.Float(string='Tare Wgt')
    job_goods_wt = fields.Float(string='Goods Wgt')
    job_gross_wt = fields.Float(string='Gross Wgt')

    commodity_id = fields.Many2one('ship.joborder', string='Commodity Details')
