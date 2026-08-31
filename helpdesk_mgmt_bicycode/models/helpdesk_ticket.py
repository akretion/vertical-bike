# Copyright 2026 Akretion (https://www.akretion.com).
# @author Raphaël Reverdy <raphael.reverdy@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

from odoo import api, fields, models


class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    bicycode_ids = fields.Many2many("stock.bicycode", string="Bicycodes")
    bicycode_count = fields.Integer(compute="_compute_bicycode_count")
    # Raw value as typed by the customer: it may not match any stock.bicycode
    # record (typo, bike not sold by us, ...).
    customer_bicycode = fields.Char(
        string="Customer-provided bicycode",
        help="Bicycode as reported by the customer, not necessarily linked "
        "to an existing Bicycode record.",
    )

    @api.depends("bicycode_ids")
    def _compute_bicycode_count(self):
        for ticket in self:
            ticket.bicycode_count = len(ticket.bicycode_ids)

    def action_view_bicycodes(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id(
            "bicycode.stock_bicycode_action"
        )
        action["domain"] = [("id", "in", self.bicycode_ids.ids)]
        action["context"] = {}
        return action

    def _bicycode_autobind(self):
        if self.customer_bicycode and not self.bicycode_ids:
            candidates = self.bicycode_ids.search([["name", "=", self.customer_bicycode]])
            if candidates:
                self.bicycode_ids = candidates
                return True
        return False

    def action_open_link_bicycode(self):
        self.ensure_one()
        # try to find bicycode ourself from customer supplied
        if self._bicycode_autobind():
            return {}
        return {
            "type": "ir.actions.act_window",
            "res_model": "helpdesk.ticket.link.bicycode.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {"default_ticket_id": self.id},
        }
