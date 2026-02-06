from odoo import models


class SeaExportWorkVolumeReport(models.AbstractModel):
    _name = "report.sea_export_work_volume.report_sea_export_work_volume"

    def _get_report_values(self, docids, data=None):
        wizard = self.env["sea.export.work.volume.wizard"].browse(docids)

        domain = []

        if wizard.date_from:
            domain.append(("hbl_arrivaldt", ">=", wizard.date_from))
        if wizard.date_to:
            domain.append(("hbl_arrivaldt", "<=", wizard.date_to))

        if wizard.branch_id:
            domain.append(("branch_id", "=", wizard.branch_id.id))

        if wizard.shipper_id:
            domain.append(("company_desc", "ilike", wizard.shipper_id.name))

        if wizard.consignee_id:
            domain.append(("company_desc", "ilike", wizard.consignee_id.name))

        if wizard.shipping_line_id:
            domain.append(("city", "ilike", wizard.shipping_line_id.name))

        if wizard.load_port_id:
            domain.append(("port_of_load_id", "=", wizard.load_port_id.id))

        if wizard.discharge_port_id:
            domain.append(("final_id", "=", wizard.discharge_port_id.id))

        shipments = self.env["ship.shipment"].search(domain)

        return {
            "company": self.env.company,
            "wizard": wizard,

            # KPI
            "total_jobs": len(shipments),
            "total_pkgs": sum(shipments.mapped("hbl_pack")),
            "total_weight": sum(shipments.mapped("hbl_weight")),
            "total_cbm": sum(shipments.mapped("hbl_volume")),

            # Financials
            "total_freight_prepaid": sum(shipments.mapped("amount_untaxed")),
            "total_freight_collect": 0.0,  # Not available in your model

            "total_other_prepaid": sum(shipments.mapped("amount_tax")),
            "total_other_collect": 0.0,  # Not available

            "total_prepaid": sum(shipments.mapped("amount_total")),
            "total_collect": 0.0,  # Not available
        }



