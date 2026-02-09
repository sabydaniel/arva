from odoo import models


class ShipQuoteVsTransactionXlsx(models.AbstractModel):
    _name = "report.ship_quote_vs_transaction.ship_quote_vs_transaction_xlsx"
    _inherit = "report.report_xlsx.abstract"

    def generate_xlsx_report(self, workbook, data, wizard):
        wizard = wizard.ensure_one()
        sheet = workbook.add_worksheet("Quotation Vs Transaction")

        title_fmt = workbook.add_format({
            "bold": True,
            "font_size": 13,
            "align": "center",
            "valign": "vcenter",
        })

        info_fmt = workbook.add_format({"font_size": 9})

        header_fmt = workbook.add_format({
            "bold": True,
            "font_size": 9,
            "align": "center",
            "valign": "vcenter",
            "bg_color": "#4472C4",
            "font_color": "#FFFFFF",
            "border": 1,
        })

        cell_fmt = workbook.add_format({
            "font_size": 9,
            "border": 1,
        })

        date_fmt = workbook.add_format({
            "font_size": 9,
            "border": 1,
            "num_format": "dd-mmm-yyyy",
        })

        widths = [16, 12, 12, 22, 14, 16, 16, 18, 14, 16, 18]
        for col, width in enumerate(widths):
            sheet.set_column(col, col, width)

        row = 0

        sheet.merge_range(row, 0, row, 10, wizard.env.company.name, title_fmt)
        row += 1
        sheet.merge_range(row, 0, row, 10, "Quotation Vs Transaction", title_fmt)
        row += 1

        sheet.merge_range(
            row, 0, row, 10,
            f"Date Range : From {wizard.date_from} To {wizard.date_to}",
            info_fmt
        )
        row += 1

        sheet.merge_range(
            row, 0, row, 10,
            f"Location : {wizard.branch_id.name if wizard.branch_id else 'All'}",
            info_fmt
        )
        row += 1

        sheet.merge_range(
            row, 0, row, 10,
            "Show : Only Valid Quotations",
            info_fmt
        )
        row += 2

        headers = [
            "Quotation Number",
            "Date",
            "Valid Till",
            "Quoted To",
            "Transaction No",
            "Quoted By",
            "Shipper",
            "Consignee",
            "Services",
            "Customer Status",
            "Status Remark",
        ]

        for col, title in enumerate(headers):
            sheet.write(row, col, title, header_fmt)

        sheet.freeze_panes(row + 1, 0)
        row += 1

        domain = []

        if wizard.date_from:
            domain.append(("quote_date", ">=", wizard.date_from))
        if wizard.date_to:
            domain.append(("quote_date", "<=", wizard.date_to))
        if wizard.department_id:
            domain.append(('department_id', '=', wizard.department_id.id))
            if wizard.status:
                domain.append(("state", "=", wizard.status))
        if wizard.quoted_to_id:
            domain.append(("client_id", "=", wizard.quoted_to_id.id))
        if wizard.branch_id:
            domain.append(("branch_id", "=", wizard.branch_id.id))

        quotes = self.env["ship.quote"].search(domain, order="quote_date")

        for q in quotes:
            sheet.write(row, 0, q.name or "", cell_fmt)
            sheet.write(row, 1, q.quote_date or "", date_fmt)
            sheet.write(row, 2, q.qutoe_enddt or "", date_fmt)
            sheet.write(row, 3, q.client_id.name or "", cell_fmt)
            sheet.write(row, 4, "", cell_fmt)
            sheet.write(row, 5, q.employee_id.name or "", cell_fmt)
            sheet.write(row, 6, q.consignor_id.name or "", cell_fmt)
            sheet.write(row, 7, q.consignee_id.name or "", cell_fmt)
            sheet.write(row, 8, q.service_id.name or "", cell_fmt)
            sheet.write(row, 9, q.state or "", cell_fmt)
            sheet.write(row, 10, q.state or "", cell_fmt)
            row += 1
