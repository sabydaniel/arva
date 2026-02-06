from odoo import models, fields

class ShipReportWizard(models.TransientModel):
    _name = 'ship.report.wizard'
    _description = 'Generate Shipping Report'

    from_date = fields.Date(required=True)
    to_date = fields.Date(required=True)

    def action_view_pdf(self):
        return self.env.ref(
            'ship_reports.action_ship_report_view'
        ).report_action(self)

    def action_print_pdf(self):
        return self.env.ref(
            'ship_reports.action_ship_report_pdf'
        ).report_action(self)

    def action_export_xlsx(self):
        return self.env.ref(
            'ship_reports.action_ship_report_xlsx'
        ).report_action(
            self,
            data={
                'from_date': self.from_date,
                'to_date': self.to_date,
            }
        )
