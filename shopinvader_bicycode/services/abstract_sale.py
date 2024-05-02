# Copyright 2023 Akretion (http://www.akretion.com)
# @author Raphaël Reverdy <raphael.reverdy@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from odoo.addons.component.core import AbstractComponent

_logger = logging.getLogger(__name__)


class AbstractSaleService(AbstractComponent):
    _inherit = [
        "shopinvader.abstract.sale.service",
    ]

    def _convert_one_line(self, line):
        res = super()._convert_one_line(line)
        res.update(
            {
                "bicycodes": (line.move_ids.move_line_ids.mapped("bicycode_ids.name")),
                # TODO remove the following line when our clients are moved
                # to a new version
                "bicycode": (
                    line.move_ids.move_line_ids.mapped("bicycode_ids.name")[:1] or [""]
                ),
            }
        )
        return res
