from odoo import models


class ShipReportXlsx(models.AbstractModel):
    _name = 'report.ship_report.ship_report_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, wizard):
        sheet = workbook.add_worksheet('Ship Report')

        headers = [
            'Shipment', 'Status', 'Created Date',
            'Income', 'Expense', 'Profit/Loss'
        ]

        for col, header in enumerate(headers):
            sheet.write(0, col, header)

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

        row = 1
        for ship in shipments:
            sheet.write(row, 0, ship.name)
            sheet.write(row, 1, ship.state)
            sheet.write(row, 2, str(ship.create_date))
            sheet.write(row, 3, ship.income)
            sheet.write(row, 4, ship.expense)
            sheet.write(row, 5, ship.profit_loss)
            row += 1
