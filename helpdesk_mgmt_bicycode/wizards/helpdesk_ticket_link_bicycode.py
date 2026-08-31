# Copyright 2026 Akretion (https://www.akretion.com).
# @author Raphaël Reverdy <raphael.reverdy@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

from odoo import Command, fields, models


class HelpdeskTicketLinkBicycodeWizard(models.TransientModel):
    _name = "helpdesk.ticket.link.bicycode.wizard"
    _description = "Link Bicycodes to Helpdesk Ticket"

    ticket_id = fields.Many2one("helpdesk.ticket", required=True, readonly=True)
    ticket_bicycode_ids = fields.Many2many(
        "stock.bicycode",
        related="ticket_id.bicycode_ids",
        readonly=True,
        string="Ticket bicycodes",
    )
    bicycode_ids = fields.Many2many(
        "stock.bicycode",
        domain="[('id', 'not in', ticket_bicycode_ids)]",
        required=True,
    )

    def action_confirm(self):
        self.ensure_one()
        if self.bicycode_ids:
            self.ticket_id.bicycode_ids = [
                Command.link(bicycode.id) for bicycode in self.bicycode_ids
            ]
