from odoo import models
from collections import defaultdict
from datetime import datetime, timedelta


class JobProfitByChargeXlsx(models.AbstractModel):
    _name = 'report.shipping_report.jobprofit_by_charge_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    _description = 'Job Profit By Charge XLSX Report'

    def generate_xlsx_report(self, workbook, data, wizard):

        sheet = workbook.add_worksheet("Job Profit By Charge")

        title_format = workbook.add_format({
            'bold': True,
            'align': 'center',
            'font_size': 14
        })

        subtitle_format = workbook.add_format({
            'bold': True,
            'align': 'center'
        })

        header_format = workbook.add_format({
            'bold': True,
            'border': 1,
            'align': 'center',
            'bg_color': '#D9D9D9'
        })

        text_format = workbook.add_format({'border': 1})

        amount_format = workbook.add_format({
            'border': 1,
            'num_format': '#,##0.00'
        })

        total_text_format = workbook.add_format({
            'bold': True,
            'top': 2
        })

        total_amount_format = workbook.add_format({
            'bold': True,
            'top': 2,
            'num_format': '#,##0.00'
        })

        sheet.set_column('A:A', 18)
        sheet.set_column('B:B', 40)
        sheet.set_column('C:C', 10)
        sheet.set_column('D:H', 18)

        row = 0
        company = self.env['res.company'].browse(data['company_id'])

        sheet.merge_range(row, 0, row, 7, company.name or '', title_format)
        row += 1

        sheet.merge_range(
            row, 0, row, 7,
            f"Job Profit Charge Code Summary for Period "
            f"{data['date_from']} to {data['date_to']}",
            subtitle_format
        )
        row += 1

        sheet.write(row, 0, f"Local Currency: {company.currency_id.name}")
        row += 1

        sheet.write(
            row, 0,
            f"Printed by {self.env.user.name} "
            f"{datetime.now().strftime('%d-%b-%Y %H:%M')}"
        )
        row += 2

        headers = [
            "Charge Code",
            "Charge Description",
            "Group",
            "Job Profit",
            "Revenues",
            "WIP",
            "Costs",
            "Accrual"
        ]

        for col, header in enumerate(headers):
            sheet.write(row, col, header, header_format)

        row += 1

        date_from = datetime.strptime(data['date_from'], "%Y-%m-%d")
        date_to = datetime.strptime(data['date_to'], "%Y-%m-%d") + timedelta(days=1)


        shipment_domain = [
            ('create_date', '>=', date_from),
            ('create_date', '<', date_to),
            ('company_id', '=', data['company_id']),
        ]

        shipments = self.env['ship.shipment'].search(shipment_domain)

        if not shipments:
            sheet.merge_range(row, 0, row, 7,
                              "No data found for selected period.",
                              text_format)
            return


        grouped = defaultdict(lambda: {
            'code': '',
            'description': '',
            'group': '',
            'revenue': 0.0,
            'cost': 0.0,
            'wip': 0.0,
            'accrual': 0.0,
        })

        for shipment in shipments:
            for ch in shipment.hbl_charges_ids:

                if not ch.charge_id:
                    continue

                product = ch.charge_id

                key = product.id

                grouped[key]['code'] = product.default_code or ''
                grouped[key]['description'] = product.name or ''

                if product.default_code and product.default_code.startswith('F'):
                    grouped[key]['group'] = 'FRT'
                elif product.default_code and product.default_code.startswith('O'):
                    grouped[key]['group'] = 'ORG'
                else:
                    grouped[key]['group'] = ''

                grouped[key]['revenue'] += ch.amount_sell or 0.0
                grouped[key]['cost'] += ch.amount_cost or 0.0
                grouped[key]['wip'] += ch.os_sell or 0.0
                grouped[key]['accrual'] += ch.os_cost or 0.0

        total_profit = total_revenue = total_cost = total_wip = total_accrual = 0.0

        for values in grouped.values():

            revenue = values['revenue']
            cost = values['cost']
            wip = values['wip']
            accrual = values['accrual']
            profit = revenue - cost

            sheet.write(row, 0, values['code'], text_format)
            sheet.write(row, 1, values['description'], text_format)
            sheet.write(row, 2, values['group'], text_format)
            sheet.write(row, 3, profit, amount_format)
            sheet.write(row, 4, revenue, amount_format)
            sheet.write(row, 5, wip, amount_format)
            sheet.write(row, 6, cost, amount_format)
            sheet.write(row, 7, accrual, amount_format)

            total_profit += profit
            total_revenue += revenue
            total_cost += cost
            total_wip += wip
            total_accrual += accrual

            row += 1

        sheet.write(row, 0, "GRAND TOTAL", total_text_format)
        sheet.write(row, 3, total_profit, total_amount_format)
        sheet.write(row, 4, total_revenue, total_amount_format)
        sheet.write(row, 5, total_wip, total_amount_format)
        sheet.write(row, 6, total_cost, total_amount_format)
        sheet.write(row, 7, total_accrual, total_amount_format)