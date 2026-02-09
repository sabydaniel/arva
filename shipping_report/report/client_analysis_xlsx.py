from odoo import models
from collections import defaultdict


class ClientAnalysisXlsx(models.AbstractModel):
    _name = "report.client_analysis_xls.client_analysis_xlsx"
    _inherit = "report.report_xlsx.abstract"

    def generate_xlsx_report(self, workbook, data, wizard):
        sheet = workbook.add_worksheet("Client Analysis")

        sheet.set_column("A:A", 12)
        sheet.set_column("B:B", 40)
        sheet.set_column("C:C", 16)
        sheet.set_column("D:E", 14)
        sheet.set_column("F:G", 20)
        sheet.set_column("H:I", 20)
        sheet.set_column("J:K", 22)

        title_fmt = workbook.add_format({
            "bold": True,
            "font_size": 14,
            "align": "left",
        })

        subtitle_fmt = workbook.add_format({
            "bold": True,
            "font_size": 11,
        })

        header_fmt = workbook.add_format({
            "bold": True,
            "border": 1,
            "align": "center",
            "valign": "vcenter",
            "text_wrap": True,
        })

        text_fmt = workbook.add_format({
            "border": 1,
            "align": "left",
            "valign": "vcenter",
        })

        center_fmt = workbook.add_format({
            "border": 1,
            "align": "center",
            "valign": "vcenter",
        })

        number_fmt = workbook.add_format({
            "border": 1,
            "align": "right",
            "valign": "vcenter",
            "num_format": "#,##0.00",
        })

        total_fmt = workbook.add_format({
            "bold": True,
            "border": 1,
            "top": 2,
            "align": "right",
            "num_format": "#,##0.00",
        })


        row = 0
        company = self.env.company

        sheet.merge_range(row, 0, row, 10, company.name, title_fmt)
        row += 1

        sheet.merge_range(
            row, 0, row, 10,
            "Forwarding - Job Analysis by Client",
            subtitle_fmt
        )
        row += 2

        sheet.merge_range(
            row, 0, row, 10,
            f"Standard Filters: From {wizard.period1_from} To {wizard.period1_to} | "
            f"From {wizard.period2_from or ''} To {wizard.period2_to or ''} | "
            f"Report By: Billing Client",
        )
        row += 2

        headers = [
            "Code",
            "Organisation Name",
            "Client Commenced",
            "Jobs Period 1",
            "Jobs Period 2",
            "Job Income Period 1",
            "Job Income Period 2",
            "Job Profit Period 1",
            "Job Profit Period 2",
            "Avg Job Profit Period 1",
            "Avg Job Profit Period 2",
        ]

        sheet.set_row(row, 32)
        for col, h in enumerate(headers):
            sheet.write(row, col, h, header_fmt)

        row += 1

        Shipment = self.env["ship.shipment"]

        domain_p1 = [
            ("hbl_date", ">=", wizard.period1_from),
            ("hbl_date", "<=", wizard.period1_to),
        ]

        domain_p2 = []
        if wizard.period2_from and wizard.period2_to:
            domain_p2 = [
                ("hbl_date", ">=", wizard.period2_from),
                ("hbl_date", "<=", wizard.period2_to),
            ]

        shipments_p1 = Shipment.search(domain_p1)
        shipments_p2 = Shipment.search(domain_p2) if domain_p2 else Shipment.browse()

        data_map = defaultdict(lambda: {
            "jobs_p1": 0,
            "jobs_p2": 0,
            "income_p1": 0.0,
            "income_p2": 0.0,
            "profit_p1": 0.0,
            "profit_p2": 0.0,
            "client_commenced": None,
        })

        def process_shipments(shipments, period_key):
            for ship in shipments:
                for ch in ship.hbl_charges_ids:
                    if not ch.debtor_id:
                        continue

                    rec = data_map[ch.debtor_id]

                    if not rec["client_commenced"]:
                        rec["client_commenced"] = ship.hbl_date

                    rec[f"jobs_{period_key}"] += 1
                    rec[f"income_{period_key}"] += ch.amount_sell or 0.0
                    rec[f"profit_{period_key}"] += (
                        (ch.amount_sell or 0.0) - (ch.amount_cost or 0.0)
                    )

        process_shipments(shipments_p1, "p1")
        process_shipments(shipments_p2, "p2")

        grand = defaultdict(float)

        for client, vals in sorted(data_map.items(), key=lambda x: x[0].name or ""):
            sheet.write(row, 0, client.ref or "", text_fmt)
            sheet.write(row, 1, client.name or "", text_fmt)
            sheet.write(row, 2, vals["client_commenced"] or "", center_fmt)

            sheet.write(row, 3, vals["jobs_p1"], center_fmt)
            sheet.write(row, 4, vals["jobs_p2"], center_fmt)

            sheet.write(row, 5, vals["income_p1"], number_fmt)
            sheet.write(row, 6, vals["income_p2"], number_fmt)

            sheet.write(row, 7, vals["profit_p1"], number_fmt)
            sheet.write(row, 8, vals["profit_p2"], number_fmt)

            avg_p1 = vals["profit_p1"] / vals["jobs_p1"] if vals["jobs_p1"] else 0.0
            avg_p2 = vals["profit_p2"] / vals["jobs_p2"] if vals["jobs_p2"] else 0.0

            sheet.write(row, 9, avg_p1, number_fmt)
            sheet.write(row, 10, avg_p2, number_fmt)

            grand["jobs_p1"] += vals["jobs_p1"]
            grand["jobs_p2"] += vals["jobs_p2"]
            grand["income_p1"] += vals["income_p1"]
            grand["income_p2"] += vals["income_p2"]
            grand["profit_p1"] += vals["profit_p1"]
            grand["profit_p2"] += vals["profit_p2"]

            row += 1


        sheet.merge_range(row, 0, row, 2, "Grand Total", total_fmt)

        sheet.write(row, 3, grand["jobs_p1"], center_fmt)
        sheet.write(row, 4, grand["jobs_p2"], center_fmt)
        sheet.write(row, 5, grand["income_p1"], total_fmt)
        sheet.write(row, 6, grand["income_p2"], total_fmt)
        sheet.write(row, 7, grand["profit_p1"], total_fmt)
        sheet.write(row, 8, grand["profit_p2"], total_fmt)

        sheet.write(
            row, 9,
            grand["profit_p1"] / grand["jobs_p1"] if grand["jobs_p1"] else 0.0,
            total_fmt
        )
        sheet.write(
            row, 10,
            grand["profit_p2"] / grand["jobs_p2"] if grand["jobs_p2"] else 0.0,
            total_fmt
        )
