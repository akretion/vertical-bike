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
        schema["lines"] = {
            "type": "list",
            "nullable": True,
            "schema": {
                "type": "dict",
                "nullable": True,
                "schema": {
                    "product_uom": {"type": "string"},
                    "product_uom_qty": {"type": "float"},
                    "state": {"type": "string"},
                    "id": {"type": "integer"},
                    "product": {
                        "type": "dict",
                        "nullable": True,
                        "schema": {
                            "product_id": {"type": "integer"},
                            "template_name": {"type": "string"},
                            "name": {"type": "string"},
                            "default_code": {"type": "string"},
                        },
                    },
                },
            },
        }
        return schema

    def _add_move_line_info(self, picking):
        parser = self._get_parser_stock_move_line()
        values = [
            move_line.jsonify(parser, one=True) for move_line in picking.move_line_ids
        ]
        return values

    def _get_parser_stock_move_line(self):
        """
        Get the parser of stock.move.line
        :return: list
        """
        to_parse = [
            "id",
            "state",
            "product_uom_qty",
            "product_uom_id:product_uom",
            ("product_id:product", ["name", "default_code", "id"]),
        ]
        return to_parse

    def _get_parser_product(self):
        """
        Get the parser of product.product
        :return: list
        """
        to_parse = [
            "id:product_id",
            "product_tmpl_id:template_name",
            "name",
            "default_code",
        ]
        return to_parse

    def _add_product_info(self, stock_move):
        """
        Add info about the related product (using product_id field).
        :param picking: stock.move
        :return: dict
        """
        product = stock_move.product_id
        if not product:
            return {}
        parser = self._get_parser_product()
        values = product.jsonify(parser, one=True)
        return values

    def _to_json_picking(self, picking):
        values = super()._to_json_picking(picking)
        values.update(
            {
                "lines": self._add_move_line_info(picking),
            }
        )
        return values
