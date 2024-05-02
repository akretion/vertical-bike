# Copyright 2023 Akretion (http://www.akretion.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    bicycode_required = fields.Boolean(
        string="Bicycode required", related="picking_id.bicycode_required"
    )


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    bicycode_required = fields.Boolean(
        string="Bicycode required", related="picking_id.bicycode_required"
    )

    bicycode_ids = fields.Many2many(
        "stock.bicycode",
        "stock_bicycode_move_line_rel",
        "move_line_id",
        "bicycode_id",
        string="Bicycodes",
    )

    def _get_aggregated_product_quantities(self, **kwargs):
        aggregated_move_lines = super()._get_aggregated_product_quantities(**kwargs)

        # unfortunately the stock.move.line::_get_aggregated_product_quantities
        # is very hard to inherit from as the key computation
        # is not inheritable. Therefore it is rewritten here for the moment
        # TODO : find a better solution
        def get_aggregated_properties(move_line):
            product_id = move_line.product_id
            name = product_id.display_name
            description = move_line.move_id.description_picking
            if description == name or description == product_id.name:
                description = False
            return (
                f'{product_id.id}_{name}{description or ""}'
                f"uom {move_line.product_uom_id.id}"
            )

        for move_line in self:
            line_key = get_aggregated_properties(move_line)
            aggregated_move_lines[line_key].setdefault(
                "bicycode_done_values", set()
            ).update([x.name for x in move_line.mapped("bicycode_ids") if x])

        return aggregated_move_lines
