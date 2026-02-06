from odoo import models

class ShipReportXlsx(models.AbstractModel):
    _name = 'report.ship_reports.ship_report_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    _description = 'Quotation List XLSX Report'

    def generate_xlsx_report(self, workbook, data, wizard):
        sheet = workbook.add_worksheet('Quotation Report')

        headers = ['Quote Number','Date','Client','Origin','Destination','Total Income','Total Expense','Profit / Loss','Profit %','Status']

        for col, header in enumerate(headers):
            sheet.write(0, col, header)

        domain = [('date', '>=', wizard.from_date),('date', '<=', wizard.to_date)]

        quotations = self.env['quotation.list'].search(domain, order='date')

        row = 1
        for q in quotations:
            sheet.write(row, 0, q.quote_number)
            sheet.write(row, 1, str(q.date))
            sheet.write(row, 2, q.client)
            sheet.write(row, 3, q.origin)
            sheet.write(row, 4, q.destination)
            sheet.write(row, 5, q.total_income)
            sheet.write(row, 6, q.total_expense)
            sheet.write(row, 7, q.total_profit_loss)
            sheet.write(row, 8, q.total_profit_loss_percent)
            sheet.write(row, 9, q.status)
            row += 1
