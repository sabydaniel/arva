from odoo import models, fields
from odoo.exceptions import ValidationError


class ShipReportWizard(models.TransientModel):
    _name = "ship.report.wizard"
    _description = "Ship Report Wizard"

    job_status = fields.Selection([
        ("draft", "Draft"),
        ("confirmed", "Confirmed"),
        ("invoiced", "Invoiced"),
        ("cancelled", "Cancelled"),
    ])

    shipment_ref = fields.Char()

    job_opened_from = fields.Date(required=True)
    job_opened_to = fields.Date(required=True)

    template_detail = fields.Boolean("Transaction Detail By Job")
    template_summary = fields.Boolean("Summary By Job")

    def _validate(self):
        if not self.template_detail and not self.template_summary:
            raise ValidationError("Select at least one template")

    def _get_shipments(self):
        domain = [
            ("hbl_depdate", ">=", self.job_opened_from),
            ("hbl_depdate", "<=", self.job_opened_to),
        ]

        if self.job_status:
            domain.append(("state", "=", self.job_status))

        if self.shipment_ref:
            domain.append(("name", "ilike", self.shipment_ref))

        return self.env["ship.shipment"].search(domain)

    def action_view(self):
        self.ensure_one()

        domain = []

        if self.job_opened_from:
            domain.append(('create_date', '>=', self.job_opened_from))
        if self.job_opened_to:
            domain.append(('create_date', '<=', self.job_opened_to))

        if self.job_status:
            domain.append(('state', '=', self.job_status))

        if self.shipment_ref:
            domain.append(('name', 'ilike', self.shipment_ref))

        return {
            'type': 'ir.actions.act_window',
            'name': 'Shipments',
            'res_model': 'ship.shipment',
            'view_mode': 'tree,form',
            'domain': domain,
            'target': 'current',
        }

    def action_print_pdf(self):
        self.ensure_one()
        if self.template_detail:
            return self.env.ref(
                'ship_report.action_ship_report_detail_pdf'
            ).report_action(self)
        else:
            return self.env.ref(
                'ship_report.action_ship_report_summary_pdf'
            ).report_action(self)

    def action_export_xlsx(self):
        self.ensure_one()
        self._validate()
        return self.env.ref(
            "ship_report.action_ship_report_xlsx"
        ).report_action(self)
