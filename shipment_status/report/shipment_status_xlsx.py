from odoo import models
from odoo.tools import format_date


class ShipmentStatusXlsx(models.AbstractModel):
    _name = "report.shipment_status.shipment_status_xlsx"
    _inherit = "report.report_xlsx.abstract"

    def _get(self, rec, field):
        return getattr(rec, field, False)

    def generate_xlsx_report(self, workbook, data, records):

        domain = data.get("domain", [])
        shipments = self.env["ship.shipment"].search(domain)

        sheet = workbook.add_worksheet("Shipment Status")

        title_fmt = workbook.add_format({
            "bold": True,
            "font_size": 18,
            "align": "center",
            "valign": "vcenter",
        })

        subtitle_fmt = workbook.add_format({
            "bold": True,
            "font_size": 12,
            "align": "center",
            "valign": "vcenter",
        })

        info_fmt = workbook.add_format({
            "font_size": 10,
            "align": "left",
            "valign": "vcenter",
        })

        header = workbook.add_format({
            "bold": True,
            "border": 1,
            "align": "center",
            "valign": "vcenter",
        })

        cell = workbook.add_format({"border": 1})

        headers = [
            "Shipment No", "Tracking No", "Shipment Date", "Cargo Type",
            "Loading Country", "Discharge Country", "Shipper", "Consignee",
            "Consol No", "Shipping Line", "HBL No", "BL No",
            "No. Of Pkg", "Unit", "Gross Wt", "Unit",
            "Chargeable Wt", "Unit", "Volume", "Unit",
            "Coload Agent", "Branch", "Status",
            "Completed Milestone Date", "Job Completed On",
        ]

        TOTAL_COLS = len(headers)

       
        sheet.merge_range(
            0, 0, 0, TOTAL_COLS - 1,
            self.env.company.name or "",
            title_fmt
        )

        sheet.merge_range(
            1, 0, 1, TOTAL_COLS - 1,
            "Sea Export Shipment Status Register",
            subtitle_fmt
        )


        row_cursor = 2

        if data.get("date_from") and data.get("date_to"):
            sheet.merge_range(
                row_cursor, 0, row_cursor, TOTAL_COLS - 1,
                "Date Range : From %s To %s" % (
                    format_date(self.env, data["date_from"]),
                    format_date(self.env, data["date_to"]),
                ),
                info_fmt
            )
            row_cursor += 1

        if data.get("branch_name"):
            sheet.merge_range(
                row_cursor, 0, row_cursor, TOTAL_COLS - 1,
                "Branch : %s" % data["branch_name"],
                info_fmt
            )
            row_cursor += 1

        HEADER_ROW = row_cursor + 1
        DATA_ROW = HEADER_ROW + 1


        for col, title in enumerate(headers):
            sheet.write(HEADER_ROW, col, title, header)
            sheet.set_column(col, col, 20)

        row = DATA_ROW
        for rec in shipments:
            col = 0

            sheet.write(row, col, self._get(rec, "name") or "", cell); col += 1
            sheet.write(row, col, self._get(rec, "tracking_no") or "", cell); col += 1

            ship_date = self._get(rec, "hbl_date")
            sheet.write(
                row, col,
                format_date(self.env, ship_date) if ship_date else "",
                cell
            ); col += 1

            sheet.write(row, col, self._get(rec, "cargo_type") or "", cell); col += 1

            load_port = self._get(rec, "port_of_load_id")
            sheet.write(row, col, load_port.name if load_port else "", cell); col += 1

            discharge_port = self._get(rec, "port_of_discharge_id")
            sheet.write(row, col, discharge_port.name if discharge_port else "", cell); col += 1

            shipper = self._get(rec, "hbl_shipper_id")
            sheet.write(row, col, shipper.name if shipper else "", cell); col += 1

            consignee = self._get(rec, "hbl_consignee_id")
            sheet.write(row, col, consignee.name if consignee else "", cell); col += 1


            while col < TOTAL_COLS:
                sheet.write(row, col, "", cell)
                col += 1

            row += 1
