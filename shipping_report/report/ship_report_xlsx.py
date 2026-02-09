from odoo import models

class ShipReportXlsx(models.AbstractModel):
    _name = "report.shipping_report.ship_profit_xlsx_template"
    _inherit = "report.report_xlsx.abstract"

    def generate_xlsx_report(self, workbook, data, objs):
        wizard = objs[0]
        company_name = wizard.env.company.name
        summary, details = wizard._get_data()

        if wizard.report_type == 'summary':
            self._create_summary_sheet(workbook, wizard, summary, company_name)
        else:
            self._create_detail_sheet(workbook, wizard, details, company_name)

    def _create_summary_sheet(self, workbook, wizard, summary, company_name):
        sheet = workbook.add_worksheet("Summary By Job")

        title = workbook.add_format({'bold': True, 'font_size': 14})
        header = workbook.add_format({'bold': True, 'border': 1, 'align': 'center', 'bg_color': '#D9D9D9'})
        text = workbook.add_format({'border': 1})
        num = workbook.add_format({'border': 1, 'num_format': '#,##0.00', 'align': 'right'})

        sheet.write(0, 0, company_name, title)
        sheet.write(1, 0, "Summary By Job", title)
        sheet.write(2, 0, f"Date: {wizard.date_from} to {wizard.date_to}")

        headers = ['Job','Ref','Branch','Dept','Status','Trans','Cont','Sales',
                   'Client','Origin','Dest','ETD','ETA','Revenue','WIP','Cost','Accrual','Profit']

        for c, h in enumerate(headers):
            sheet.write(4, c, h, header)

        total_revenue = total_wip = total_cost = total_accrual = total_profit = 0.0

        row = 5
        for l in summary:
            sheet.write(row, 0, l.get('job',''), text)
            sheet.write(row, 1, l.get('ref',''), text)
            sheet.write(row, 2, l.get('branch',''), text)
            sheet.write(row, 3, l.get('dept',''), text)
            sheet.write(row, 4, l.get('status',''), text)
            sheet.write(row, 5, l.get('trans',''), text)
            sheet.write(row, 6, l.get('cont',''), text)
            sheet.write(row, 7, l.get('sales',''), text)
            sheet.write(row, 8, l.get('client',''), text)
            sheet.write(row, 9, l.get('origin',''), text)
            sheet.write(row,10, l.get('dest',''), text)
            sheet.write(row,11, l.get('etd',''), text)
            sheet.write(row,12, l.get('eta',''), text)

            revenue = l.get('revenue',0)
            wip = l.get('wip',0)
            cost = l.get('cost',0)
            accrual = l.get('accrual',0)
            profit = l.get('profit',0)

            sheet.write(row,13, revenue, num)
            sheet.write(row,14, wip, num)
            sheet.write(row,15, cost, num)
            sheet.write(row,16, accrual, num)
            sheet.write(row,17, profit, num)

            total_revenue += revenue
            total_wip += wip
            total_cost += cost
            total_accrual += accrual
            total_profit += profit

            row += 1

        sheet.write(row, 12, "TOTAL", header)
        sheet.write(row, 13, total_revenue, num)
        sheet.write(row, 14, total_wip, num)
        sheet.write(row, 15, total_cost, num)
        sheet.write(row, 16, total_accrual, num)
        sheet.write(row, 17, total_profit, num)

    def _create_detail_sheet(self, workbook, wizard, details, company_name):
        sheet = workbook.add_worksheet("Transaction Detail")

        title = workbook.add_format({'bold': True, 'font_size': 14})
        header = workbook.add_format(
            {'bold': True, 'border': 1, 'align': 'center', 'bg_color': '#4472C4', 'font_color': 'white'})
        text = workbook.add_format({'border': 1})
        num = workbook.add_format({'border': 1, 'num_format': '#,##0.00', 'align': 'right'})
        bold = workbook.add_format({'bold': True, 'border': 1})

        sheet.write(0, 0, company_name, title)
        sheet.write(1, 0, "Transaction Detail By Job", title)
        sheet.write(2, 0, f"Date: {wizard.date_from} to {wizard.date_to}")

        headers = ['Type', 'Charge', 'Posted', 'Br', 'Dept', 'Org', 'Invoice',
                   'Amount', 'Revenue', 'WIP', 'Cost', 'Accrual', 'Job Profit']
        for c, h in enumerate(headers):
            sheet.write(4, c, h, header)

        row = 5

        gt_rev = gt_wip = gt_cost = gt_acc = gt_profit = 0
        for job_key, lines in details.items():

            sheet.merge_range(
                row, 0, row, 12,
                f"Job : {job_key} | Branch: {lines[0]['br']} | Client: {lines[0]['org']}",
                bold
            )

            row += 1
            jr = jw = jc = ja = jp = 0

            for l in lines:
                sheet.write(row, 0, l['type'], text)
                sheet.write(row, 1, l['charge'], text)
                sheet.write(row, 2, l['posted'], text)
                sheet.write(row, 3, l['br'], text)
                sheet.write(row, 4, l['dept'], text)
                sheet.write(row, 5, l['org'], text)
                sheet.write(row, 6, l['invoice'], text)
                sheet.write(row, 7, l['amount'], num)
                sheet.write(row, 8, l['revenue'], num)
                sheet.write(row, 9, l['wip'], num)
                sheet.write(row, 10, l['cost'], num)
                sheet.write(row, 11, l['accrual'], num)
                sheet.write(row, 12, l['job_profit'], num)

                jr += l['revenue']
                jw += l['wip']
                jc += l['cost']
                ja += l['accrual']
                jp += l['job_profit']

                row += 1

            sheet.write(row, 6, "JOB TOTAL", bold)
            sheet.write(row, 8, jr, num)
            sheet.write(row, 9, jw, num)
            sheet.write(row, 10, jc, num)
            sheet.write(row, 11, ja, num)
            sheet.write(row, 12, jp, num)
            row += 2

            gt_rev += jr
            gt_wip += jw
            gt_cost += jc
            gt_acc += ja
            gt_profit += jp

        sheet.write(row, 6, "TOTAL", bold)
        sheet.write(row, 8, gt_rev, num)
        sheet.write(row, 9, gt_wip, num)
        sheet.write(row, 10, gt_cost, num)
        sheet.write(row, 11, gt_acc, num)
        sheet.write(row, 12, gt_profit, num)