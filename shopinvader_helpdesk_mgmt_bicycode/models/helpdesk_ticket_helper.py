# Copyright 2026 Akretion (https://www.akretion.com).
# @author Raphaël Reverdy <raphael.reverdy@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

from odoo import models


class HelpdeskTicketHelper(models.AbstractModel):
    _inherit = "shopinvader_api_helpdesk.helpdesk_router.helper"

    def create(self, values):
        record = super().create(values)
        # sudo needed: the authenticated partner has no write access on
        # stock.bicycode / helpdesk.ticket.bicycode_ids
        record.sudo()._bicycode_autobind()
        return record
