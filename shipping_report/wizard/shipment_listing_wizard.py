from odoo import models, fields, api
from odoo.osv import expression


class ShipmentListingWizard(models.TransientModel):
    _name = "shipment.listing.wizard"
    _description = "Shipment Listing Wizard"


    company_id = fields.Many2one(
        "res.company",
        string="Company",
        required=True,
        default=lambda self: self.env.company,
    )

    branch_id = fields.Many2one(
        "res.company",
        string="Branch",
        required=True,
        domain="[('parent_id', '=', company_id)]",
    )

    client_id = fields.Many2one(
        "res.partner",
        string="Client",
        domain=[("customer_rank", ">", 0), ("is_company", "=", True)],
    )

    is_consignor = fields.Boolean(default=True)
    is_consignee = fields.Boolean(default=True)
    is_billing_client = fields.Boolean(default=True)

    freight_direction = fields.Selection(
        [
            ("all", "All"),
            ("import", "Import"),
            ("export", "Export"),
        ],
        string="Freight Direction",
        default="all",
    )

    shipment_transport = fields.Selection(
        [
            ("air", "Air"),
            ("sea", "Sea"),
            ("road", "Road"),
        ],
        string="Transport",
    )

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        branch = self.env.user.branch_ids[:1]
        if branch:
            res["branch_id"] = branch.id
            res["company_id"] = branch.parent_id.id or self.env.company.id
        return res

    @api.onchange("company_id")
    def _onchange_company(self):
        self.branch_id = False

    @api.onchange("branch_id")
    def _onchange_branch(self):
        if self.branch_id and self.branch_id.parent_id:
            self.company_id = self.branch_id.parent_id


    def action_preview(self):
        self.ensure_one()
        return self.env.ref(
            "shipping_report.action_shipment_listing_preview"
        ).report_action(self)

    def action_print_pdf(self):
        self.ensure_one()
        return self.env.ref(
            "shipping_report.action_shipment_listing_pdf"
        ).report_action(self)

    def action_print_xlsx(self):
        self.ensure_one()
        return self.env.ref(
            "shipping_report.shipment_listing_xlsx"
        ).report_action(self)


    def _get_shipments(self):
        self.ensure_one()

        domain = [
            ("company_id", "=", self.company_id.id),
        ]


        if self.branch_id:
            domain.append(("branch_id", "=", self.branch_id.id))


        if self.shipment_transport:
            transport = self.env["ship.transport"].search(
                [("name", "ilike", self.shipment_transport)],
                limit=1
            )
            if transport:
                domain.append(("transport_id", "=", transport.id))
            else:
                return self.env["ship.shipment"].browse([])


        company_country = self.company_id.country_id

        if self.freight_direction == "import" and company_country:
            domain.append(
                ("hbl_portdisch_id.country_id", "=", company_country.id)
            )

        elif self.freight_direction == "export" and company_country:
            domain.append(
                ("hbl_portload_id.country_id", "=", company_country.id)
            )

        if self.client_id:
            role_conditions = []

            if self.is_consignor:
                role_conditions.append(("hbl_consigner_id", "=", self.client_id.id))

            if self.is_consignee:
                role_conditions.append(("hbl_consignee_id", "=", self.client_id.id))

            if self.is_billing_client:
                role_conditions.append(("hbl_customer_id", "=", self.client_id.id))

            if not role_conditions:
                return self.env["ship.shipment"].browse([])

            domain = expression.AND([
                domain,
                expression.OR([[cond] for cond in role_conditions])
            ])

        return self.env["ship.shipment"].search(
            domain,
            order="hbl_depdate desc",
        )