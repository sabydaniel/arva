# -*- coding: utf-8 -*-
from odoo import models


class JobCountSummaryXlsx(models.AbstractModel):
    _name = 'report.job_count_summary.job_count_summary_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    _description = 'Job Count Summary XLSX Report'

    def generate_xlsx_report(self, workbook, data, wizards):

        sheet = workbook.add_worksheet('Job Count Summary')


        title = workbook.add_format({
            'bold': True,
            'font_size': 14,
        })

        sub = workbook.add_format({
            'bold': True,
            'font_size': 10,
        })

        head = workbook.add_format({
            'bold': True,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'text_wrap': True,
            'font_size': 9,
        })

        left = workbook.add_format({
            'border': 1,
            'align': 'left',
            'font_size': 9,
        })

        center = workbook.add_format({
            'border': 1,
            'align': 'center',
            'font_size': 9,
        })

        num = workbook.add_format({
            'border': 1,
            'align': 'right',
            'num_format': '#,##0',
            'font_size': 9,
        })

        dec2 = workbook.add_format({
            'border': 1,
            'align': 'right',
            'num_format': '#,##0.00',
            'font_size': 9,
        })

        dec3 = workbook.add_format({
            'border': 1,
            'align': 'right',
            'num_format': '#,##0.000',
            'font_size': 9,
        })

        bold = workbook.add_format({
            'bold': True,
            'border': 1,
            'font_size': 9,
        })

        bold_num = workbook.add_format({
            'bold': True,
            'border': 1,
            'align': 'right',
            'num_format': '#,##0',
            'font_size': 9,
        })

        bold_dec2 = workbook.add_format({
            'bold': True,
            'border': 1,
            'align': 'right',
            'num_format': '#,##0.00',
            'font_size': 9,
        })

        bold_dec3 = workbook.add_format({
            'bold': True,
            'border': 1,
            'align': 'right',
            'num_format': '#,##0.000',
            'font_size': 9,
        })

        sheet.set_column('A:A', 12)
        sheet.set_column('B:B', 15)
        sheet.set_column('C:D', 10)
        sheet.set_column('E:H', 14)
        sheet.set_column('I:K', 12)


        wizard = wizards[0]
        row = 0

        sheet.write(row, 0, wizard.env.company.name, title)
        row += 1
        sheet.write(row, 0, 'Job Count Summary by Branch', title)
        row += 1

        info = f"Job Opened: {wizard.date_from.strftime('%d-%b-%y')} - {wizard.date_to.strftime('%d-%b-%y')}"
        if wizard.branch_id:
            info += f" | Branch: {wizard.branch_id.name}"
        sheet.write(row, 0, info, sub)
        row += 2


        headers = [
            'Branch', 'Department', 'Freight', 'Mode',
            'Accounting', 'Shipments', 'Standalone',
            'Ship + Decl', 'FCL TEU', 'W/V', 'AIR KG'
        ]

        for col, h in enumerate(headers):
            sheet.write(row, col, h, head)

        sheet.set_row(row, 32)
        row += 1


        report_data = wizard._get_report_data()

        for branch in report_data['branches']:

            sheet.merge_range(row, 0, row, 10, f"BRANCH : {branch['branch_code']}", bold)
            row += 1

            for r in branch['rows']:
                sheet.write(row, 0, branch['branch_code'], left)
                sheet.write(row, 1, r['department'], left)
                sheet.write(row, 2, r['freight_direction'], center)
                sheet.write(row, 3, r['transport_mode'], center)
                sheet.write(row, 4, r['accounting_job_headers'], num)
                sheet.write(row, 5, r['job_headers_on_shipments'], num)
                sheet.write(row, 6, r.get('job_headers_standalone', 0), num)
                sheet.write(row, 7, r.get('job_headers_with_declarations', 0), num)
                sheet.write(row, 8, r.get('shipment_fcl_teu', 0), dec2)
                sheet.write(row, 9, r.get('shipment_chargeable_wv', 0), dec3)
                sheet.write(row, 10, r.get('shipment_air_kg', 0), dec3)
                row += 1

            sheet.merge_range(row, 0, row, 3, f"Total {branch['branch_code']}", bold)
            sheet.write(row, 4, branch['totals']['accounting_job_headers'], bold_num)
            sheet.write(row, 5, branch['totals']['job_headers_on_shipments'], bold_num)
            sheet.write(row, 6, branch['totals'].get('job_headers_standalone', 0), bold_num)
            sheet.write(row, 7, branch['totals'].get('job_headers_with_declarations', 0), bold_num)
            sheet.write(row, 8, branch['totals'].get('shipment_fcl_teu', 0), bold_dec2)
            sheet.write(row, 9, branch['totals'].get('shipment_chargeable_wv', 0), bold_dec3)
            sheet.write(row, 10, branch['totals'].get('shipment_air_kg', 0), bold_dec3)
            row += 1


        sheet.merge_range(row, 0, row, 3, 'GRAND TOTAL', bold)
        sheet.write(row, 4, report_data['grand_total']['accounting_job_headers'], bold_num)
        sheet.write(row, 5, report_data['grand_total']['job_headers_on_shipments'], bold_num)
        sheet.write(row, 6, report_data['grand_total'].get('job_headers_standalone', 0), bold_num)
        sheet.write(row, 7, report_data['grand_total'].get('job_headers_with_declarations', 0), bold_num)
        sheet.write(row, 8, report_data['grand_total'].get('shipment_fcl_teu', 0), bold_dec2)
        sheet.write(row, 9, report_data['grand_total'].get('shipment_chargeable_wv', 0), bold_dec3)
        sheet.write(row, 10, report_data['grand_total'].get('shipment_air_kg', 0), bold_dec3)
