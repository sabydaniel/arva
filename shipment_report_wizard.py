from odoo import api, fields, models, _
from odoo.exceptions import UserError
import io
import base64
from datetime import datetime, timedelta
import xlsxwriter
from odoo.tools.misc import xlsxwriter
from odoo.exceptions import UserError


class ShipmentReportWizard(models.TransientModel):
    _name = 'shipment.report.wizard'
    _description = 'Shipment Report Wizard'

    from_date = fields.Date(string="From Date", required=True)
    to_date = fields.Date(string="To Date", required=True)
    customer_id = fields.Many2one('res.partner', string="Customer")

    #
    def action_generate_xlsx_report(self):
        print("XL Report")
        return self.env.ref('shipping.shipment_report_xlsx_action').report_action(self)

class ShipmentReportXlsx(models.AbstractModel):
    _name = 'report.shipping.shipment_xlsx'
    _description = 'Shipment Report'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, objs):
        wizard = objs[0]
        shipments = self.env['ship.shipment'].search([
            ('hbl_date', '>=', wizard.from_date),
            ('hbl_date', '<=', wizard.to_date),
            ('hbl_customer_id', '=', wizard.customer_id.id),
        ])

        sheet = workbook.add_worksheet('Shipment Report')
        title_format = workbook.add_format({
            'bold': True,
            'font_size': 14,
            'align': 'center',
            'valign': 'vcenter'
        })
        header_format = workbook.add_format({'bold': True, 'align': 'center', 'bg_color': '#D3D3D3', 'border': 1})
        cell_format = workbook.add_format({'border': 1})

        # Add the title row
        title_text = f"Shipment Report from {wizard.from_date.strftime('%Y-%m-%d')} to {wizard.to_date.strftime('%Y-%m-%d')}"
        sheet.merge_range('A1:J1', title_text, title_format)

        # Column headers
        headers = ['Shipment No', 'Date', 'Customer', 'Sales Person', 'Charge Name', 'Currency', 'Cost', 'Sell', 'Tax',
                   'Total']
        for col, header in enumerate(headers):
            sheet.write(1, col, header, header_format)

        row = 2  # Start data from the third row
        grand_total = 0

        for shipment in shipments:
            sheet.write(row, 0, shipment.name, cell_format)
            sheet.write(row, 1, shipment.hbl_date.strftime('%Y-%m-%d') if shipment.hbl_date else '', cell_format)
            sheet.write(row, 2, shipment.hbl_customer_id.name, cell_format)
            sheet.write(row, 3, shipment.employee_id.name if shipment.employee_id else '', cell_format)

            shipment_total = 0
            charge_row = row

            for charge in shipment.hbl_charges_ids:
                sheet.write(charge_row, 4, charge.charge_id.name if charge.charge_id else '', cell_format)
                sheet.write(charge_row, 5, charge.currency_id.name, cell_format)
                sheet.write(charge_row, 6, charge.estimated_cost, cell_format)
                sheet.write(charge_row, 7, charge.estimated_sell, cell_format)
                sheet.write(charge_row, 8, charge.sell_tax_amount, cell_format)
                sheet.write(charge_row, 9, charge.amount_sell, cell_format)

                shipment_total += charge.amount_sell
                charge_row += 1

            sheet.write(row, 9, shipment_total, cell_format)
            grand_total += shipment_total
            row = max(row + 1, charge_row)

        sheet.write(row, 8, 'Grand Total:', header_format)
        sheet.write(row, 9, grand_total, header_format)
