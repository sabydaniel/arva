from odoo import models
from odoo.tools import format_date


class ShipmentStatusXlsx(models.AbstractModel):
    _name = "report.shipping_report.shipment_status_xlsx"
    _inherit = "report.report_xlsx.abstract"
    _description = "Sea Export Shipment Status Register XLSX"

    def generate_xlsx_report(self, workbook, data, records):

        data = data or {}
        domain = data.get("domain") or []


        if not isinstance(domain, list):
            domain = []

        shipments = self.env["ship.shipment"].search(domain)


        print("DOMAIN:", domain)
        print("SHIPMENT COUNT:", len(shipments))

        sheet = workbook.add_worksheet("Shipment Status")

        title_fmt = workbook.add_format({
            "bold": True,
            "font_size": 18,
            "align": "center",
        })

        subtitle_fmt = workbook.add_format({
            "bold": True,
            "font_size": 12,
            "align": "center",
        })

        info_fmt = workbook.add_format({
            "font_size": 10,
            "align": "left",
        })

        header_fmt = workbook.add_format({
            "bold": True,
            "border": 1,
            "align": "center",
        })

        cell_fmt = workbook.add_format({
            "border": 1,
        })

        headers = [
            "Shipment No",
            "Shipment Date",
            "Department",
            "Transport",
            "ETD",
            "ETA",
            "Carrier",
            "HBL No",
            "Master BL",
            "Shipper",
            "Consignee",
            "Customer",
            "POL",
            "POD",
            "Weight",
            "Volume",
            "Status",
        ]

        total_cols = len(headers)


        sheet.merge_range(
            0, 0, 0, total_cols - 1,
            self.env.company.name or "",
            title_fmt
        )


        sheet.merge_range(
            1, 0, 1, total_cols - 1,
            "Sea Export Shipment Status Register",
            subtitle_fmt
        )

        row_cursor = 2


        if data.get("date_from") and data.get("date_to"):
            sheet.merge_range(
                row_cursor, 0, row_cursor, total_cols - 1,
                "Date Range : From %s To %s" % (
                    format_date(self.env, data["date_from"]),
                    format_date(self.env, data["date_to"]),
                ),
                info_fmt
            )
            row_cursor += 1


        if data.get("branch_name"):
            sheet.merge_range(
                row_cursor, 0, row_cursor, total_cols - 1,
                "Branch : %s" % data["branch_name"],
                info_fmt
            )
            row_cursor += 1

        header_row = row_cursor + 1
        data_row = header_row + 1

        for col, title in enumerate(headers):
            sheet.write(header_row, col, title, header_fmt)
            sheet.set_column(col, col, 20)

        row = data_row


        for rec in shipments:

            col = 0

            sheet.write(row, col, rec.name or "", cell_fmt); col += 1

            sheet.write(
                row, col,
                format_date(self.env, rec.hbl_date) if rec.hbl_date else "",
                cell_fmt
            ); col += 1

            sheet.write(row, col, rec.department_id.name if rec.department_id else "", cell_fmt); col += 1
            sheet.write(row, col, rec.transport_id.name if rec.transport_id else "", cell_fmt); col += 1

            sheet.write(
                row, col,
                format_date(self.env, rec.hbl_depdate) if rec.hbl_depdate else "",
                cell_fmt
            ); col += 1

            sheet.write(
                row, col,
                format_date(self.env, rec.hbl_arrivaldt) if rec.hbl_arrivaldt else "",
                cell_fmt
            ); col += 1

            sheet.write(row, col, rec.hbl_carrier_id.name if rec.hbl_carrier_id else "", cell_fmt); col += 1
            sheet.write(row, col, rec.hbl_housebill or "", cell_fmt); col += 1
            sheet.write(row, col, rec.hbl_masterbill or "", cell_fmt); col += 1

            sheet.write(row, col, rec.hbl_consigner_id.name if rec.hbl_consigner_id else "", cell_fmt); col += 1
            sheet.write(row, col, rec.hbl_consignee_id.name if rec.hbl_consignee_id else "", cell_fmt); col += 1
            sheet.write(row, col, rec.hbl_customer_id.name if rec.hbl_customer_id else "", cell_fmt); col += 1

            sheet.write(row, col, rec.hbl_portload_id.name if rec.hbl_portload_id else "", cell_fmt); col += 1
            sheet.write(row, col, rec.hbl_portdisch_id.name if rec.hbl_portdisch_id else "", cell_fmt); col += 1

            sheet.write(row, col, rec.hbl_weight or 0.0, cell_fmt); col += 1
            sheet.write(row, col, rec.hbl_volume or 0.0, cell_fmt); col += 1

            sheet.write(row, col, rec.state or "", cell_fmt); col += 1

            row += 1