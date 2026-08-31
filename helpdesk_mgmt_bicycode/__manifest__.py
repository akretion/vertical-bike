# Copyright 2026 Akretion (https://www.akretion.com).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

{
    "name": "Helpdesk Bicycode",
    "summary": "Link Bicycodes to helpdesk tickets",
    "version": "18.0.1.0.0",
    "category": "Helpdesk",
    "website": "https://github.com/akretion/vertical-bike",
    "author": "Akretion",
    "maintainers": ["hparfr"],
    "license": "AGPL-3",
    "depends": [
        "helpdesk_mgmt",
        "bicycode",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/helpdesk_ticket_views.xml",
        "views/stock_bicycode_views.xml",
        "wizards/helpdesk_ticket_link_bicycode_views.xml",
    ],
}
