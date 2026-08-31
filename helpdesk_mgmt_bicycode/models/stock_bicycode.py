# Copyright 2026 Akretion (https://www.akretion.com).
# @author Raphaël Reverdy <raphael.reverdy@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

from odoo import fields, models


class StockBicycode(models.Model):
    _inherit = "stock.bicycode"

    ticket_ids = fields.Many2many("helpdesk.ticket", string="Helpdesk tickets")
