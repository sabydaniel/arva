from odoo import models, fields


class SeaExportWorkVolumeWizard(models.TransientModel):
    _name = "sea.export.work.volume.wizard"
    _description = "Sea Export Work Volume Wizard"

    date_from = fields.Date("From Date")
    date_to = fields.Date("To Date")

    type = fields.Selection([
        ("summary", "Summary"),
    ], default="summary", string="Type")

    branch_id = fields.Many2one("res.company", string="Branch")

    shipper_id = fields.Many2one("res.partner", "Shipper")
    consignee_id = fields.Many2one("res.partner", "Consignee")
    shipping_line_id = fields.Many2one("res.partner", "Shipping Line")

    consol_type = fields.Selection([
        ("all", "All"),
        ("back_to_back", "Back To Back"),
        ("agent", "Agent"),
    ], default="all", string="Consol Type")

    cargo_type = fields.Selection([
        ("all", "All"),
        ("fcl", "FCL"),
        ("lcl", "LCL"),
    ], default="all", string="Cargo Type")

    load_port_id = fields.Many2one("res.country.state", string="Load Port")
    discharge_port_id = fields.Many2one("res.country.state", string="Discharge Port")

    def action_generate_pdf(self):
          return self.env.ref(
                "sea_export_work_volume.action_report_sea_export_work_volume"
            ).report_action(self)
