from odoo import models, fields
from odoo.exceptions import UserError
import base64
import io
import openpyxl


class OrganizationImportWizard(models.TransientModel):
    _name = 'organization.import.wizard'
    _description = 'Organization Import Wizard'

    file = fields.Binary(string="Upload XLSX", required=True)
    file_name = fields.Char()

    def action_import(self):

        if not self.file:
            raise UserError("Please upload Excel file.")

        try:
            file_data = base64.b64decode(self.file)
            workbook = openpyxl.load_workbook(io.BytesIO(file_data))
            sheet = workbook.active
        except Exception:
            raise UserError("Invalid file format.")

        for row in sheet.iter_rows(min_row=2, values_only=True):

            if not row:
                continue

            code = str(row[0]).strip() if row[0] else False
            name = str(row[1]).strip() if len(row) > 1 and row[1] else ""
            rec = str(row[2]).strip().upper() if len(row) > 2 and row[2] else ""
            pay = str(row[3]).strip().upper() if len(row) > 3 and row[3] else ""

            if not code:
                continue

            organization = self.env['shipping.organization'].search([
                ('code', '=', code)
            ], limit=1)

            values = {
                'name': name,
                'code': code,
                'receivable_acct': rec == 'Y',
                'payable_acct': pay == 'Y',
            }

            if organization:

                organization.write(values)
            else:

                self.env['shipping.organization'].create(values)


        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
