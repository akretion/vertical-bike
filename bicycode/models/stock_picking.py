# Copyright 2023 Akretion (http://www.akretion.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, fields, models
from odoo.exceptions import UserError


class PickingType(models.Model):
    _inherit = "stock.picking.type"

    bicycode_required = fields.Boolean(
        string="Bicycode required",
        default=False,
        help="If checked, the user will have to input the bicycode of the "
        "products that have one to validate the picking.",
    )


class Picking(models.Model):
    _inherit = "stock.picking"

    bicycode_required = fields.Boolean(
        string="Bicycode required", related="picking_type_id.bicycode_required"
    )

    def button_validate(self):
        rv = super().button_validate()
        if rv is not True:
            return rv

        self._check_bicycode()
        return rv

    def _check_bicycode(self):
        for picking in self:
            if not picking.picking_type_id.bicycode_required:
                continue
            for move in picking.move_lines:
                if not move.product_id.has_bicycode:
                    continue
                for move_line in move.move_line_ids:
                    if move_line.qty_done > len(move_line.bicycode_ids):
                        raise UserError(
                            _("You must input %d bicycode(s) for product %s")
                            % (move_line.qty_done, move_line.product_id.name)
                        )
                    if move_line.qty_done < len(move_line.bicycode_ids):
                        raise UserError(
                            _("You have set too many bicycodes for product %s")
                            % move_line.product_id.name
                        )
        return True
