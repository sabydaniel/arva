from odoo import models

class ShipReportDetailPdf(models.AbstractModel):
    _name = 'report.ship_report.ship_report_detail_qweb'
    _description = 'Ship Report Detail PDF'

    def _get_domain(self, wizard):
        domain = []

        if wizard.job_opened_from:
            domain.append(('create_date', '>=', wizard.job_opened_from))
        if wizard.job_opened_to:
            domain.append(('create_date', '<=', wizard.job_opened_to))
        if wizard.job_status:
            domain.append(('state', '=', wizard.job_status))
        if wizard.shipment_ref:
            domain.append(('name', 'ilike', wizard.shipment_ref))

        return domain

    def _get_report_values(self, docids, data=None):
        wizard = self.env['ship.report.wizard'].browse(docids[0])

        shipments = self.env['ship.shipment'].search(
            self._get_domain(wizard)
        )

        return {
            'doc_ids': docids,
            'doc_model': 'ship.report.wizard',
            'wizard': wizard,
            'shipments': shipments,
        }


class ShipReportSummaryPdf(models.AbstractModel):
    _name = 'report.ship_report.ship_report_summary_qweb'
    _description = 'Ship Report Summary PDF'

    def _get_report_values(self, docids, data=None):
        wizard = self.env['ship.report.wizard'].browse(docids[0])

        domain = []

        if wizard.job_opened_from:
            domain.append(('create_date', '>=', wizard.job_opened_from))
        if wizard.job_opened_to:
            domain.append(('create_date', '<=', wizard.job_opened_to))
        if wizard.job_status:
            domain.append(('state', '=', wizard.job_status))
        if wizard.shipment_ref:
            domain.append(('name', 'ilike', wizard.shipment_ref))

        shipments = self.env['ship.shipment'].search(domain)

        return {
            'doc_ids': docids,
            'doc_model': 'ship.report.wizard',
            'wizard': wizard,
            'shipments': shipments,
        }
