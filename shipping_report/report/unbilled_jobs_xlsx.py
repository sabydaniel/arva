from odoo import models


class UnbilledJobsXlsx(models.AbstractModel):
    _name = 'report.shipping_report.unbilled_jobs_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, records):

        sheet = workbook.add_worksheet('Unbilled Jobs')

        title_format = workbook.add_format({
            'bold': True,
            'font_size': 14,
            'align': 'center'
        })

        header_format = workbook.add_format({
            'bold': True,
            'bg_color': '#2F75B5',
            'color': 'white',
            'border': 1,
            'align': 'center'
        })

        text_format = workbook.add_format({'border': 1})
        date_format = workbook.add_format({
            'num_format': 'dd-mm-yyyy',
            'border': 1
        })

        sheet.merge_range('A1:P1', records and records[0].branch_id.name, title_format)
        headers = [
            'Module',
            'Job Type',
            'Customer Remark',
            'Sales Person',
            'Customer',
            'Job No',
            'Job Date',
            'Mode',
            'Load Port',
            'Destination',
            'Shipper',
            'Consignee',
            'Location',
            'BE/SB Type',
            'Status',
            'Status Date'
        ]

        row = 2
        col = 0

        for header in headers:
            sheet.write(row, col, header, header_format)
            col += 1

        row += 1

        for rec in records:

            col = 0

            sheet.write(row, col, rec.department_id.name or '', text_format);
            col += 1
            sheet.write(row, col, rec.type_id.name or '', text_format);
            col += 1
            sheet.write(row, col, rec.hbl_desc or '', text_format);
            col += 1
            sheet.write(row, col, rec.employee_id.name or '', text_format);
            col += 1
            sheet.write(row, col, rec.hbl_customer_id.name or '', text_format);
            col += 1

            sheet.write(row, col, rec.name or '', text_format);
            col += 1

            if rec.hbl_date:
                sheet.write(row, col, rec.hbl_date, date_format)
            else:
                sheet.write(row, col, '', text_format)
            col += 1

            sheet.write(row, col, rec.mode_id.name or '', text_format);
            col += 1
            sheet.write(row, col, rec.hbl_portload_id.name or '', text_format);
            col += 1
            sheet.write(row, col, rec.final_id.name or '', text_format);
            col += 1
            sheet.write(row, col, rec.hbl_consigner_id.name or '', text_format);
            col += 1
            sheet.write(row, col, rec.hbl_consignee_id.name or '', text_format);
            col += 1
            sheet.write(row, col, rec.branch_id.name or '', text_format);
            col += 1
            sheet.write(row, col, rec.hbl_reltype or '', text_format);
            col += 1
            sheet.write(row, col, rec.state or '', text_format);
            col += 1

            if rec.write_date:
                sheet.write(row, col, rec.write_date, date_format)
            else:
                sheet.write(row, col, '', text_format)

            row += 1