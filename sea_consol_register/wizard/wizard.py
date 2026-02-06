from odoo import models, fields

class SeaConsolWizard(models.TransientModel):
    _name = "sea.consol.wizard"
    _description = "Sea Export Consol Register Wizard"

    date_from = fields.Date("Consol Date From")
    date_to = fields.Date("Consol Date To")

    branch_id = fields.Many2one("res.company", string="Branch")
    department_id = fields.Many2one("hr.department", string="Department")

    shipping_line_id = fields.Many2one("res.partner", string="Shipping Line")

    consol_type = fields.Selection([
        ("back_to_back", "Back To Back"),
        ("agent", "Agent's Consolidation")
    ], string="Consol Type")

    cargo_type = fields.Selection([
        ("fcl", "FCL"),
        ("lcl", "LCL")
    ], string="Cargo Type")

    port_of_load_id = fields.Many2one("res.country.state", string="Load Port")
    port_of_discharge_id = fields.Many2one("res.country.state", string="Disch. Port")

    status = fields.Selection([
        ("draft", "Draft"),
        ("confirmed", "Confirmed"),
        ("completed", "Completed"),
        ("cancel", "Cancelled")
    ], default="completed", string="Status")

    def generate_xlsx(self):
        domain = []

        if self.date_from:
            domain.append(("create_date", ">=", self.date_from))

        if self.date_to:
            domain.append(("create_date", "<=", self.date_to))

        if self.port_of_load_id:
            domain.append(("port_of_load_id", "=", self.port_of_load_id.id))

        if self.port_of_discharge_id:
            domain.append(("port_of_discharge_id", "=", self.port_of_discharge_id.id))

        return {
            "type": "ir.actions.report",
            "report_type": "xlsx",
            "report_name": "sea_consol_register.simple_xlsx",
            "data": {
                "domain": domain,
                "date_from": self.date_from,
                "date_to": self.date_to,
                "branch": self.branch_id.name if self.branch_id else "",
            },
        }