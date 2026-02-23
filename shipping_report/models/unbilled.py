from odoo import models, fields, api

class ShipShipment(models.Model):
    _inherit = 'ship.shipment'

    is_invoiced = fields.Boolean(
        string="Invoiced",
        compute="_compute_invoice_status",
        store=True
    )

    is_purchased = fields.Boolean(
        string="Purchased",
        compute="_compute_purchase_status",
        store=True
    )

    def _compute_invoice_status(self):
        for rec in self:
            invoices = self.env['account.move'].search_count([
                ('invoice_origin', '=', rec.name),
                ('move_type', 'in', ('out_invoice', 'out_refund')),
                ('state', '=', 'posted')
            ])
            rec.is_invoiced = bool(invoices)

    def _compute_purchase_status(self):
        for rec in self:
            purchases = self.env['purchase.order'].search_count([
                ('origin', '=', rec.name),
                ('state', 'in', ('purchase', 'done'))
            ])
            rec.is_purchased = bool(purchases)
