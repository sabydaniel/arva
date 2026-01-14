import base64
from odoo import models, fields, _
from odoo.exceptions import UserError

class ShipmentReportWizard(models.TransientModel):
    _name = 'shipment.report.wizard'
    _description = 'Shipment Report Wizard'

    date_from = fields.Date(required=True)
    date_to = fields.Date(required=True)

    def _get_shipments(self):
        return self.env['ship.shipment'].search([
            ('create_date', '>=', self.date_from),
            ('create_date', '<=', self.date_to),
        ])

    def action_send(self):
        shipments = self._get_shipments()
        if not shipments:
            raise UserError("No shipments found for selected dates.")

        report_xmlid = 'shipping_reports_wizard.action_shipment_report_pdf'
        attachments = self.env['ir.attachment']

        for shipment in shipments:
            pdf, _content_type = self.env['ir.actions.report']._render_qweb_pdf(
                report_xmlid,
                res_ids=[shipment.id]
            )

            attachments |= self.env['ir.attachment'].create({
                'name': f'Shipment_{shipment.name}.pdf',
                'type': 'binary',
                'datas': base64.b64encode(pdf),
                'mimetype': 'application/pdf',
                'res_model': 'ship.shipment',
                'res_id': shipment.id,
            })

        template = self.env.ref(
            'shipping_reports_wizard.mail_template_shipment_report',
            raise_if_not_found=False
        )

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'mail.compose.message',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_use_template': bool(template),
                'default_template_id': template.id if template else False,
                'default_subject': 'Shipment Reports',
                'default_body': 'Please find attached shipment documents.',
                'default_attachment_ids': [(6, 0, attachments.ids)],
                'default_composition_mode': 'comment',
            }
        }