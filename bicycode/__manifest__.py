# Copyright 2023 Akretion
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

{
    "name": "Bicycode",
    "summary": "Bicycode management",
    "version": "14.0.2.0.0",
    "category": "Stock",
    "website": "https://github.com/akretion/vertical-bike",
    "author": "Akretion",
    "maintainers": ["hparfr"],
    "application": True,
    "license": "AGPL-3",
    "depends": [
        "stock",
        "sale",
    ],
    "data": [
        "security/bicycode_security.xml",
        "security/ir.model.access.csv",
        "views/stock_move_views.xml",
        "views/product_views.xml",
        "views/stock_bicycode_views.xml",
        "views/stock_picking_views.xml",
        "views/stock_move_line_views.xml",
        "report/report_deliveryslip.xml",
    ],
}
