# Copyright 2023 Akretion (http://www.akretion.com)
# @author Raphaël Reverdy <raphael.reverdy@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.addons.component.core import Component


class DeliveryService(Component):
    _inherit = "shopinvader.delivery.service"

    def _get_picking_schema(self):
        """
        :return: dict
        """
        schema = super()._get_picking_schema()
        schema["lines"]["schema"]["schema"]["bicycodes"] = {
            "type": "list",
            "nullable": False,
            "schema": {
                "type": "string",
            },
        }
        return schema

    def _get_parser_stock_move_line(self):
        vals = super()._get_parser_stock_move_line()
        vals.append(
            ("bicycode_ids:bicycodes"),
        )
        return vals
