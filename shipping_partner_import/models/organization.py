from odoo import models, fields

class ShippingOrganization(models.Model):
    _name = "shipping.organization"
    _description = "Shipping Organization"

    name = fields.Char(required=True)
    code = fields.Char(required=True)
    is_company = fields.Boolean(default=True)

    receivable_acct = fields.Boolean(string="Receivable")
    payable_acct = fields.Boolean(string="Payable")

    def action_open_import_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Import Organization',
            'res_model': 'organization.import.wizard',
            'view_mode': 'form',
            'target': 'new',
        }
