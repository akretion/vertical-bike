# Copyright 2023 Akretion (http://www.akretion.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class StockBicycode(models.Model):
    _name = "stock.bicycode"
    _description = "Bicycode is an id on a bike frame"

    name = fields.Char("Bicycode")

    move_line_ids = fields.Many2many(
        "stock.move.line",
        "stock_bicycode_move_line_rel",
        "bicycode_id",
        "move_line_id",
        string="Move lines",
    )

    sale_order_ids = fields.Many2many(
        "sale.order",
        string="Sale orders",
        compute="_compute_sale_order_ids",
        store=True,
    )

    partner_ids = fields.Many2many(
        "res.partner",
        string="Partners",
        compute="_compute_partner_ids",
        store=True,
    )

    picking_ids = fields.Many2many(
        "stock.picking",
        string="Pickings",
        compute="_compute_picking_ids",
        store=True,
    )

    @api.depends("move_line_ids")
    def _compute_partner_ids(self):
        for record in self:
            record.partner_ids = record.move_line_ids.mapped("move_id.partner_id")

    @api.depends("move_line_ids")
    def _compute_sale_order_ids(self):
        for record in self:
            record.sale_order_ids = record.move_line_ids.mapped(
                "move_id.sale_line_id.order_id"
            )

    @api.depends("move_line_ids")
    def _compute_picking_ids(self):
        for record in self:
            record.picking_ids = record.move_line_ids.mapped("move_id.picking_id")
