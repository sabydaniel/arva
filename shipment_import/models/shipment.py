from odoo import models, fields

class Shipment(models.Model):
    _name = 'shipment.shipment'
    _description = 'Shipment'

    name = fields.Char(string="Shipment Reference")
    shipment_date = fields.Date(string="Date")
    customer = fields.Char(string="Customer")
    sales_person = fields.Char(string="Sales Person")
    vessel = fields.Char(string="Vessel")
    voyage_number = fields.Char(string="Voyage Number")
    master_bill = fields.Char(string="Master Bill")
    house_bill = fields.Char(string="House Bill")
    origin = fields.Char(string="Origin")
    destination = fields.Char(string="Destination")
    marks = fields.Text(string="Marks & Numbers")
    description = fields.Text(string="Description")

    charge_ids = fields.One2many(
        'shipment.charge',
        'shipment_id',
        string="Charges"
    )


class ShipmentCharge(models.Model):
    _name = 'shipment.charge'
    _description = 'Shipment Charges'

    shipment_id = fields.Many2one(
        'shipment.shipment',
        string="Shipment"
    )

    description = fields.Char(string="Charge")
    cost = fields.Float(string="Estimated Cost")
    sell = fields.Float(string="Estimated Sell")
