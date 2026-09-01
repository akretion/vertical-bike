# Copyright 2026 Akretion (https://www.akretion.com).
# @author Raphaël Reverdy <raphael.reverdy@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

from odoo.addons.shopinvader_schema_helpdesk.schemas import (
    HelpdeskTicket as BaseHelpdeskTicket,
)


class HelpdeskTicket(BaseHelpdeskTicket, extends=True):
    customer_bicycode: str | None = None

    def to_helpdesk_ticket_vals(self) -> dict:
        vals = super().to_helpdesk_ticket_vals()
        vals["customer_bicycode"] = self.customer_bicycode
        return vals

    @classmethod
    def from_helpdesk_ticket(cls, odoo_rec):
        obj = super().from_helpdesk_ticket(odoo_rec)
        obj.customer_bicycode = odoo_rec.customer_bicycode or None
        return obj
