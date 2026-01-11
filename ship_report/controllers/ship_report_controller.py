from odoo import http
from odoo.http import request


class ShipReportController(http.Controller):

    @http.route('/ship_report/html', type='http', auth='user', website=False)
    def ship_report_html(self, **kwargs):
        wizard_id = int(kwargs.get('wizard_id'))
        wizard = request.env['ship.report.wizard'].browse(wizard_id)

        domain = []

        if wizard.job_opened_from:
            domain.append(('create_date', '>=', wizard.job_opened_from))
        if wizard.job_opened_to:
            domain.append(('create_date', '<=', wizard.job_opened_to))

        if wizard.job_status:
            domain.append(('state', '=', wizard.job_status))

        if wizard.shipment_ref:
            domain.append(('name', 'ilike', wizard.shipment_ref))

        shipments = request.env['ship.shipment'].search(domain)

        return request.render(
            'ship_report.ship_report_html_template',
            {
                'shipments': shipments,
                'wizard': wizard,
            }
        )
