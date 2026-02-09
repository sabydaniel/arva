# from odoo import models
# from odoo.tools import format_date
#
#
# class ShipmentRevenueXlsx(models.AbstractModel):
#     _name = 'report.shipment_revenue.shipment_revenue_xlsx'
#     _inherit = 'report.report_xlsx.abstract'
#     _description = 'Sea Export Shipment Register - Revenue XLS'
#
#     def generate_xlsx_report(self, workbook, data, records):
#
#         domain = data.get('domain', []).copy()
#
#         date_from = data.get('date_from')
#         date_to = data.get('date_to')
#         branch_name = data.get('branch_name', '')
#
#         if date_from:
#             domain.append(('hbl_date', '>=', date_from))
#         if date_to:
#             domain.append(('hbl_date', '<=', date_to))
#
#         shipments = self.env['ship.shipment'].search(domain)
#
#
#         sheet = workbook.add_worksheet('Shipment Revenue')
#
#         title_fmt = workbook.add_format({
#             'bold': True,
#             'font_size': 14,
#             'align': 'center',
#             'valign': 'vcenter',
#         })
#
#         subtitle_fmt = workbook.add_format({
#             'bold': True,
#             'font_size': 12,
#             'align': 'center',
#             'valign': 'vcenter',
#         })
#
#         info_fmt = workbook.add_format({
#             'bold': True,
#             'font_size': 10,
#             'align': 'left',
#         })
#
#         header = workbook.add_format({
#             'bold': True,
#             'border': 1,
#             'align': 'center',
#             'valign': 'vcenter',
#         })
#
#         cell = workbook.add_format({'border': 1})
#
#         TOTAL_COLS = 24
#
#
#         company_name = self.env.company.name or ''
#         sheet.merge_range(0, 0, 0, TOTAL_COLS - 1, company_name, title_fmt)
#         sheet.merge_range(
#             1, 0, 1, TOTAL_COLS - 1,
#             'Sea Export Shipment Register - Revenue',
#             subtitle_fmt
#         )
#
#
#         date_text = ''
#         if date_from and date_to:
#             date_text = f"Date Range : From {format_date(self.env, date_from)} To {format_date(self.env, date_to)}"
#         elif date_from:
#             date_text = f"Date : {format_date(self.env, date_from)}"
#
#         sheet.merge_range(2, 0, 2, TOTAL_COLS - 1, date_text, info_fmt)
#
#         if branch_name:
#             sheet.merge_range(3, 0, 3, TOTAL_COLS - 1, f"Branch : {branch_name}", info_fmt)
#
#
#         headers = [
#             'Shipment No', 'Tracking No', 'Container Nos', 'Booking Thru',
#             'Discharge Port', 'ETD', 'Goods Description', 'Consignee',
#             'Estimated Revenue', 'Estimated Cost', 'Shipment Date',
#             'Loading Port', 'BL No', 'Container Type', 'Customer Remark',
#             'Estimated Profit', 'Cargo Type', 'Consol Type', 'Status',
#             'Shipping Line', 'Branch', 'Vessel/Voyage', 'HBL No', 'Shipper',
#         ]
#
#         header_row = 4
#         data_row = 5
#
#         for col, title in enumerate(headers):
#             sheet.write(header_row, col, title, header)
#             sheet.set_column(col, col, 20)
#
#
#         row = data_row
#         for rec in shipments:
#             sheet.write(row, 0, rec.name or '', cell)
#             sheet.write(row, 1, getattr(rec, 'tracking_no', '') or '', cell)
#             sheet.write(row, 2, getattr(rec, 'container_nos', '') or '', cell)
#             sheet.write(row, 3, getattr(rec, 'booking_thru', '') or '', cell)
#
#             sheet.write(
#                 row, 4,
#                 rec.port_of_discharge_id.name
#                 if getattr(rec, 'port_of_discharge_id', False) else '',
#                 cell
#             )
#
#
#             sheet.write(
#                 row, 5,
#                 format_date(self.env, rec.hbl_date)
#                 if getattr(rec, 'hbl_date', False) else '',
#                 cell
#             )
#
#             sheet.write(row, 6, getattr(rec, 'goods_description', '') or '', cell)
#
#             sheet.write(
#                 row, 7,
#                 rec.hbl_consignee_id.name
#                 if getattr(rec, 'hbl_consignee_id', False) else '',
#                 cell
#             )
#
#             sheet.write(row, 8, getattr(rec, 'income', 0.0) or 0.0, cell)
#             sheet.write(row, 9, getattr(rec, 'expense', 0.0) or 0.0, cell)
#
#
#             sheet.write(
#                 row, 10,
#                 format_date(self.env, rec.hbl_date)
#                 if getattr(rec, 'hbl_date', False) else '',
#                 cell
#             )
#
#             sheet.write(
#                 row, 11,
#                 rec.port_of_load_id.name
#                 if getattr(rec, 'port_of_load_id', False) else '',
#                 cell
#             )
#
#             sheet.write(row, 12, getattr(rec, 'bl_no', '') or '', cell)
#             sheet.write(row, 13, getattr(rec, 'container_type', '') or '', cell)
#             sheet.write(row, 14, getattr(rec, 'customer_remark', '') or '', cell)
#             sheet.write(row, 15, getattr(rec, 'profit', 0.0) or 0.0, cell)
#             sheet.write(row, 16, getattr(rec, 'cargo_type', '') or '', cell)
#             sheet.write(row, 17, getattr(rec, 'consol_type', '') or '', cell)
#             sheet.write(row, 18, getattr(rec, 'state', '') or '', cell)
#
#             sheet.write(
#                 row, 19,
#                 rec.shipping_line_id.name
#                 if getattr(rec, 'shipping_line_id', False) else '',
#                 cell
#             )
#
#             sheet.write(
#                 row, 20,
#                 rec.branch_id.name
#                 if getattr(rec, 'branch_id', False) else '',
#                 cell
#             )
#
#             sheet.write(row, 21, getattr(rec, 'vessel_voyage', '') or '', cell)
#             sheet.write(row, 22, getattr(rec, 'hbl_no', '') or '', cell)
#
#             sheet.write(
#                 row, 23,
#                 rec.hbl_shipper.name
#                 if getattr(rec, 'hbl_shipper', False) else '',
#                 cell
#             )
#
#             row += 1
from odoo import models
from odoo.tools import format_date


class ShipmentRevenueXlsx(models.AbstractModel):
    _name = 'report.shipment_revenue.shipment_revenue_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    _description = 'Sea Export Shipment Register - Revenue XLS'

    def generate_xlsx_report(self, workbook, data, records):
        domain = data.get('domain', []).copy()

        date_from = data.get('date_from')
        date_to = data.get('date_to')
        branch_name = data.get('branch_name', '')

        if date_from:
            domain.append(('hbl_date', '>=', date_from))
        if date_to:
            domain.append(('hbl_date', '<=', date_to))

        shipments = self.env['ship.shipment'].search(domain)

        sheet = workbook.add_worksheet('Shipment Revenue')

        title_fmt = workbook.add_format({
            'bold': True,
            'font_size': 14,
            'align': 'center',
            'valign': 'vcenter',
        })

        subtitle_fmt = workbook.add_format({
            'bold': True,
            'font_size': 12,
            'align': 'center',
            'valign': 'vcenter',
        })

        info_fmt = workbook.add_format({
            'bold': True,
            'font_size': 10,
            'align': 'left',
        })

        header = workbook.add_format({
            'bold': True,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
        })

        cell = workbook.add_format({'border': 1})

        TOTAL_COLS = 24

        company_name = self.env.company.name or ''
        sheet.merge_range(0, 0, 0, TOTAL_COLS - 1, company_name, title_fmt)
        sheet.merge_range(
            1, 0, 1, TOTAL_COLS - 1,
            'Sea Export Shipment Register - Revenue',
            subtitle_fmt
        )

        date_text = ''
        if date_from and date_to:
            date_text = f"Date Range : From {format_date(self.env, date_from)} To {format_date(self.env, date_to)}"
        elif date_from:
            date_text = f"Date : {format_date(self.env, date_from)}"

        sheet.merge_range(2, 0, 2, TOTAL_COLS - 1, date_text, info_fmt)

        if branch_name:
            sheet.merge_range(3, 0, 3, TOTAL_COLS - 1, f"Branch : {branch_name}", info_fmt)

        headers = [
            'Shipment No', 'Tracking No', 'Container Nos', 'Booking Thru',
            'Discharge Port', 'ETD', 'Goods Description', 'Consignee',
            'Estimated Revenue', 'Estimated Cost', 'Shipment Date',
            'Loading Port', 'BL No', 'Container Type', 'Customer Remark',
            'Estimated Profit', 'Cargo Type', 'Consol Type', 'Status',
            'Shipping Line', 'Branch', 'Vessel/Voyage', 'HBL No', 'Shipper',
        ]

        header_row = 4
        data_row = 5

        for col, title in enumerate(headers):
            sheet.write(header_row, col, title, header)
            sheet.set_column(col, col, 20)

        row = data_row
        for rec in shipments:
            sheet.write(row, 0, rec.name or '', cell)
            sheet.write(row, 1, getattr(rec, 'tracking_no', '') or '', cell)
            sheet.write(row, 2, getattr(rec, 'container_nos', '') or '', cell)
            sheet.write(row, 3, getattr(rec, 'booking_thru', '') or '', cell)

            sheet.write(
                row, 4,
                rec.port_of_discharge_id.name if rec.port_of_discharge_id else '',
                cell
            )

            sheet.write(
                row, 5,
                format_date(self.env, rec.hbl_date) if rec.hbl_date else '',
                cell
            )

            sheet.write(row, 6, getattr(rec, 'goods_description', '') or '', cell)

            sheet.write(
                row, 7,
                rec.hbl_consignee_id.name if rec.hbl_consignee_id else '',
                cell
            )

            sheet.write(row, 8, rec.income or 0.0, cell)
            sheet.write(row, 9, rec.expense or 0.0, cell)

            sheet.write(
                row, 10,
                format_date(self.env, rec.hbl_date) if rec.hbl_date else '',
                cell
            )

            sheet.write(
                row, 11,
                rec.port_of_load_id.name if rec.port_of_load_id else '',
                cell
            )

            sheet.write(row, 12, getattr(rec, 'bl_no', '') or '', cell)
            sheet.write(row, 13, getattr(rec, 'container_type', '') or '', cell)
            sheet.write(row, 14, getattr(rec, 'customer_remark', '') or '', cell)
            sheet.write(row, 15, rec.profit_loss or 0.0, cell)
            sheet.write(row, 16, getattr(rec, 'cargo_type', '') or '', cell)
            sheet.write(row, 17, getattr(rec, 'consol_type', '') or '', cell)
            sheet.write(row, 18, rec.state or '', cell)

            sheet.write(
                row, 19,
                rec.shipping_line_id.name if rec.shipping_line_id else '',
                cell
            )

            sheet.write(
                row, 20,
                rec.branch_id.name if rec.branch_id else '',
                cell
            )

            sheet.write(row, 21, getattr(rec, 'vessel_voyage', '') or '', cell)
            sheet.write(row, 22, getattr(rec, 'hbl_housebill', '') or '', cell)


            sheet.write(
                row, 23,
                rec.hbl_consigner_id.name if rec.hbl_consigner_id else '',
                cell
            )

            row += 1
