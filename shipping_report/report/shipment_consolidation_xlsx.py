from odoo import models
from odoo.tools import format_date


class ShipmentConsolidationXlsx(models.AbstractModel):
    _name = "report.shipping_report.shipment_consolidation_xlsx"
    _inherit = "report.report_xlsx.abstract"
    _description = "Shipment Consolidation XLS"

    def generate_xlsx_report(self, workbook, data, wizard):

        domain = data.get("domain", [])
        shipments = self.env["ship.shipment"].search(domain)

        sheet = workbook.add_worksheet("Consolidation")

        title_fmt = workbook.add_format({
            "bold": True,
            "font_size": 14,
            "align": "center",
        })

        header_fmt = workbook.add_format({
            "bold": True,
            "border": 1,
            "align": "center",
            "valign": "vcenter",
        })

        cell_fmt = workbook.add_format({"border": 1})

        date_fmt = workbook.add_format({
            "border": 1,
            "num_format": "dd-mmm-yyyy"
        })

        company_name = self.env.company.name or ""

        TOTAL_COLS = 25  # 0 to 24


        sheet.merge_range(0, 0, 0, TOTAL_COLS - 1, company_name, title_fmt)

        sheet.merge_range(
            1, 0, 1, TOTAL_COLS - 1,
            "Sea Export Shipment to be Consolidated",
            title_fmt
        )

        date_from = data.get("date_from")
        date_to = data.get("date_to")
        branch = data.get("branch_name", "")

        date_text = ""
        if date_from and date_to:
            date_text = f"Date Range : From {format_date(self.env, date_from)} To {format_date(self.env, date_to)}"
        elif date_from:
            date_text = f"Date : {format_date(self.env, date_from)}"

        sheet.merge_range(
            2, 0, 2, TOTAL_COLS - 1,
            f"{date_text}    Branch : {branch}",
            workbook.add_format({"bold": True})
        )

        row = 4

        headers = [
            "Shipment No", "Tracking No", "Container Nos.",
            "Loading Country", "Booking Thru", "Discharge Port",
            "ETD", "Job Order No.", "Good Desc",
            "Consignee", "Discharge Country",
            "Customer", "Shipment Date", "Loading Port",
            "BL NO", "Sales Person", "Customer Remark",
            "Dest. Agent", "Cargo Type", "Consol Type",
            "Status", "Shipping Line", "Vessel/Voyage",
            "HBL No", "Shipper"
        ]

        for col, header in enumerate(headers):
            sheet.write(row, col, header, header_fmt)

        row += 1

        for rec in shipments:

            sheet.write(row, 0, rec.name or '', cell_fmt)
            sheet.write(row, 1, rec.hbl_jobno or '', cell_fmt)
            sheet.write(row, 2, rec.container_id.name if rec.container_id else '', cell_fmt)
            sheet.write(row, 3, rec.country_id.name if rec.country_id else '', cell_fmt)
            sheet.write(row, 4, rec.booking_id.name if rec.booking_id else '', cell_fmt)
            sheet.write(row, 5, rec.hbl_portdisch_id.name if rec.hbl_portdisch_id else '', cell_fmt)

            if rec.hbl_depdate:
                sheet.write_datetime(row, 6, rec.hbl_depdate, date_fmt)
            else:
                sheet.write(row, 6, '', cell_fmt)

            sheet.write(row, 7, rec.hbl_jobno or '', cell_fmt)
            sheet.write(row, 8, rec.hbl_desc or '', cell_fmt)
            sheet.write(row, 9, rec.hbl_consignee_id.name if rec.hbl_consignee_id else '', cell_fmt)
            sheet.write(row, 10, rec.hbl_consignee_country_id.name if rec.hbl_consignee_country_id else '', cell_fmt)
            sheet.write(row, 11, rec.hbl_customer_id.name if rec.hbl_customer_id else '', cell_fmt)

            if rec.hbl_date:
                sheet.write_datetime(row, 12, rec.hbl_date, date_fmt)
            else:
                sheet.write(row, 12, '', cell_fmt)

            sheet.write(row, 13, rec.hbl_portload_id.name if rec.hbl_portload_id else '', cell_fmt)
            sheet.write(row, 14, rec.hbl_masterbill or '', cell_fmt)
            sheet.write(row, 15, rec.employee_id.name if rec.employee_id else '', cell_fmt)
            sheet.write(row, 16, rec.hbl_mark or '', cell_fmt)
            sheet.write(row, 17, rec.hbl_destagent_id.name if rec.hbl_destagent_id else '', cell_fmt)
            sheet.write(row, 18, rec.transport_id.name if rec.transport_id else '', cell_fmt)
            sheet.write(row, 19, "Agent Consol", cell_fmt)
            sheet.write(row, 20, rec.state or '', cell_fmt)
            sheet.write(row, 21, rec.hbl_carrier_id.name if rec.hbl_carrier_id else '', cell_fmt)
            sheet.write(row, 22, rec.hbl_vessel_id.name if rec.hbl_vessel_id else '', cell_fmt)
            sheet.write(row, 23, rec.hbl_housebill or '', cell_fmt)
            sheet.write(row, 24, rec.hbl_customer_id.name if rec.hbl_customer_id else '', cell_fmt)

            row += 1

        sheet.set_column(0, TOTAL_COLS - 1, 18)
