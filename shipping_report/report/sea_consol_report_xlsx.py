from odoo import models
from odoo.tools import format_date

class SeaConsolXlsx(models.AbstractModel):
    _name = "report.shipping_report.simple_xlsx"
    _inherit = "report.report_xlsx.abstract"

    def generate_xlsx_report(self, workbook, data, records):
        domain = data.get("domain", [])
        shipments = self.env["ship.shipment"].search(domain)

        sheet = workbook.add_worksheet("Sea Export Consol")

        def val(rec, field):
            return getattr(rec, field, "") if hasattr(rec, field) else ""

        def m2o(rec, field):
            if hasattr(rec, field) and getattr(rec, field):
                return getattr(rec, field).name
            return ""

        title_fmt = workbook.add_format({
            "bold": True, "font_size": 14, "align": "center"
        })
        subtitle_fmt = workbook.add_format({
            "bold": True, "font_size": 12, "align": "center"
        })
        left_fmt = workbook.add_format({"font_size": 10})
        header_fmt = workbook.add_format({
            "bold": True, "border": 1, "align": "center"
        })
        cell_fmt = workbook.add_format({"border": 1})

        TOTAL_COLS = 29

        company_name = self.env.company.name
        sheet.merge_range(0, 0, 0, TOTAL_COLS - 1, company_name, title_fmt)
        sheet.merge_range(1, 0, 1, TOTAL_COLS - 1,
                          "Sea Export Consol Register", subtitle_fmt)

        sheet.write(2, 0,
                    f"Date Range : From {data.get('date_from','')} "
                    f"To {data.get('date_to','')}    "
                    f"Branch : {data.get('branch','')}",
                    left_fmt)

        headers = [
            "Consol No",
            "Consol Date",
            "Consol Type",
            "Origin Agent",
            "Destination Agent",
            "Loading Country",
            "Discharge Country",
            "Vessel/Voyage No",
            "Shipping Line",
            "Load Port",
            "Disch Port",
            "BL No",
            "TotOuterPkgs_QTY",
            "Unit",
            "TotGrWt_QTY",
            "Unit",
            "Chargeable Wt",
            "Unit",
            "Container No",
            "Chrgwt_Vol_QTY",
            "Unit",
            "Branch",
            "Freight Type",
            "ETD",
            "Shipment No",
            "House No",
            "Cargo Type",
            "Financials Locked On",
            "Operations Locked On",
        ]

        row = 4
        for col, h in enumerate(headers):
            sheet.write(row, col, h, header_fmt)
            sheet.set_column(col, col, 18)

        row += 1
        for s in shipments:
            sheet.write(row, 0, s.name or "", cell_fmt)                     # Consol No
            sheet.write(row, 1, format_date(self.env, s.create_date.date())
                        if s.create_date else "", cell_fmt)                # Consol Date
            sheet.write(row, 2, val(s, "consol_type"), cell_fmt)
            sheet.write(row, 3, m2o(s, "origin_agent_id"), cell_fmt)
            sheet.write(row, 4, m2o(s, "destination_agent_id"), cell_fmt)
            sheet.write(row, 5, m2o(s, "loading_country_id"), cell_fmt)
            sheet.write(row, 6, m2o(s, "discharge_country_id"), cell_fmt)
            sheet.write(row, 7, val(s, "vessel_voyage"), cell_fmt)
            sheet.write(row, 8, m2o(s, "shipping_line_id"), cell_fmt)
            sheet.write(row, 9, m2o(s, "port_of_load_id"), cell_fmt)
            sheet.write(row,10, m2o(s, "port_of_discharge_id"), cell_fmt)
            sheet.write(row,11, val(s, "bl_no"), cell_fmt)
            sheet.write(row,12, val(s, "total_packages"), cell_fmt)
            sheet.write(row,13, "", cell_fmt)
            sheet.write(row,14, val(s, "gross_weight"), cell_fmt)
            sheet.write(row,15, "", cell_fmt)
            sheet.write(row,16, val(s, "chargeable_weight"), cell_fmt)
            sheet.write(row,17, "", cell_fmt)
            sheet.write(row,18, val(s, "container_no"), cell_fmt)
            sheet.write(row,19, val(s, "volume_weight"), cell_fmt)
            sheet.write(row,20, "", cell_fmt)
            sheet.write(row,21, m2o(s, "branch_id"), cell_fmt)
            sheet.write(row,22, val(s, "freight_type"), cell_fmt)
            sheet.write(row,23, format_date(self.env, s.etd)
                        if hasattr(s, "etd") and s.etd else "", cell_fmt)
            sheet.write(row,24, s.name or "", cell_fmt)
            sheet.write(row,25, val(s, "hbl_no"), cell_fmt)
            sheet.write(row,26, val(s, "cargo_type"), cell_fmt)
            sheet.write(row,27, val(s, "financial_lock_date"), cell_fmt)
            sheet.write(row,28, val(s, "operation_lock_date"), cell_fmt)

            row += 1
