from odoo import models, api

class ShipReportPDF(models.AbstractModel):
    _name = "report.shipping_report.ship_profit_pdf_template"
    _description = "Job Profit PDF Report"

    @api.model
    def _get_report_values(self, docids, data=None):
        wizard = self.env['ship.report.wizard'].browse(docids[:1])

        summary = []
        details = {}

        if wizard:
            summary, details = wizard._get_data()

        return {
            'doc_ids': wizard.ids,
            'doc_model': 'ship.report.wizard',
            'docs': wizard,
            'wizard': wizard,
            'summary': summary,
            'details': details,
            'company': wizard.env.company,
        }
