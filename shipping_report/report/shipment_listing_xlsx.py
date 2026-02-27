from odoo import models


class ShipmentListingXlsx(models.AbstractModel):
    _name = "report.shipping_report.shipment_listing_xlsx"
    _inherit = "report.report_xlsx.abstract"
    _description = "Shipment Listing XLSX Report"

    def generate_xlsx_report(self, workbook, data, wizard):

        sheet = workbook.add_worksheet("Shipment Listing")

        header = workbook.add_format({
            "bold": True,
            "border": 1,
            "align": "center",
            "valign": "vcenter",
            "bg_color": "#D9D9D9",
        })

        cell = workbook.add_format({
            "border": 1,
            "valign": "vcenter",
        })

        date_cell = workbook.add_format({
            "border": 1,
            "valign": "vcenter",
            "num_format": "dd-mm-yyyy",
        })

        headers = [
            "Shipment",
            "Consignor",
            "Consignee",
            "Customer",
            "Mode",
            "Transport",
            "ETD",
            "ETA",
            "POL",
            "POD",
        ]

        for col, title in enumerate(headers):
            sheet.write(0, col, title, header)
            sheet.set_column(col, col, 20)

        row = 1
        shipments = wizard._get_shipments()

        for ship in shipments:
            sheet.write(row, 0, ship.name or "", cell)
            sheet.write(row, 1, ship.hbl_consigner_id.name or "", cell)
            sheet.write(row, 2, ship.hbl_consignee_id.name or "", cell)
            sheet.write(row, 3, ship.hbl_customer_id.name or "", cell)
            sheet.write(row, 4, ship.mode_id.name or "", cell)
            sheet.write(row, 5, ship.transport_id.name or "", cell)

            if ship.hbl_depdate:
                sheet.write(row, 6, ship.hbl_depdate, date_cell)
            else:
                sheet.write(row, 6, "", cell)

            if ship.hbl_arrivaldt:
                sheet.write(row, 7, ship.hbl_arrivaldt, date_cell)
            else:
                sheet.write(row, 7, "", cell)

            sheet.write(row, 8, ship.hbl_portload_id.name or "", cell)
            sheet.write(row, 9, ship.hbl_portdisch_id.name or "", cell)

            row += 1