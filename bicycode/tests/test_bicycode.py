from odoo.exceptions import UserError
from odoo.tests import Form, common, tagged


@tagged("post_install", "-at_install")
class TestBicycode(common.TransactionCase):
    def setUp(self):
        super(TestBicycode, self).setUp()

        self.company = self.env.ref("base.main_company")

        self.partner_a = self.env["res.partner"].create(
            {"name": "Partner A", "email": "partner.a@example.com"}
        )
        self.product_a = self.env["product.product"].create(
            {
                "name": "product_a",
                "uom_id": self.env.ref("uom.product_uom_unit").id,
                "lst_price": 1000.0,
                "standard_price": 800.0,
            }
        )
        self.product_b = self.env["product.product"].create(
            {
                "name": "product_b",
                "uom_id": self.env.ref("uom.product_uom_dozen").id,
                "lst_price": 200.0,
                "standard_price": 160.0,
            }
        )
        self.so = self.env["sale.order"].create(
            {
                "partner_id": self.partner_a.id,
                "partner_invoice_id": self.partner_a.id,
                "partner_shipping_id": self.partner_a.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "name": p.name,
                            "product_id": p.id,
                            "product_uom_qty": 4,
                            "product_uom": p.uom_id.id,
                            "price_unit": p.list_price,
                        },
                    )
                    for p in (
                        self.product_a,
                        self.product_b,
                    )
                ],
                "picking_policy": "direct",
            }
        )
        so_copy = self.so.copy()
        so_copy.action_confirm()
        self.picking_type = so_copy.picking_ids.picking_type_id

    def test_bicycode_not_required_not_on_product_not_specified(self):
        self.so.action_confirm()
        pick = self.so.picking_ids
        self.assertEqual(pick.picking_type_id, self.picking_type)

        pick.move_lines.write({"quantity_done": 3})
        wiz_act = pick.button_validate()
        wiz = Form(
            self.env[wiz_act["res_model"]].with_context(wiz_act["context"])
        ).save()
        wiz.process()
        self.assertEqual(pick.state, "done")

    def test_bicycode_required_not_on_product_not_specified(self):
        self.picking_type.bicycode_required = True
        self.so.action_confirm()
        pick = self.so.picking_ids
        self.assertEqual(pick.picking_type_id, self.picking_type)

        pick.move_lines.write({"quantity_done": 3})
        wiz_act = pick.button_validate()
        wiz = Form(
            self.env[wiz_act["res_model"]].with_context(wiz_act["context"])
        ).save()
        wiz.process()
        self.assertEqual(pick.state, "done")

    def test_bicycode_not_required_but_on_product_not_specified(self):
        self.product_a.has_bicycode = True
        self.so.action_confirm()
        pick = self.so.picking_ids
        self.assertEqual(pick.picking_type_id, self.picking_type)

        pick.move_lines.write({"quantity_done": 3})
        wiz_act = pick.button_validate()
        wiz = Form(
            self.env[wiz_act["res_model"]].with_context(wiz_act["context"])
        ).save()
        wiz.process()
        self.assertEqual(pick.state, "done")

    def test_bicycode_required_on_product_with_bicycode_lower_amount(self):
        self.picking_type.bicycode_required = True
        self.product_a.has_bicycode = True

        self.so.action_confirm()
        pick = self.so.picking_ids
        pick.move_lines.write({"quantity_done": 3})
        wiz_act = pick.button_validate()
        wiz = Form(
            self.env[wiz_act["res_model"]].with_context(wiz_act["context"])
        ).save()
        with self.assertRaisesRegex(
            UserError, r"You must input 3 bicycode\(s\) for product product_a"
        ):
            wiz.process()

    def test_bicycode_required_on_product_with_bicycode_good_amount(self):
        self.picking_type.bicycode_required = True
        self.product_a.has_bicycode = True

        self.so.action_confirm()
        pick = self.so.picking_ids
        pick.move_lines.write({"quantity_done": 3})
        pick.move_line_ids[0].bicycode_ids = [
            (0, 0, {"name": "bicycode_%d" % i}) for i in range(3)
        ]
        wiz_act = pick.button_validate()
        wiz = Form(
            self.env[wiz_act["res_model"]].with_context(wiz_act["context"])
        ).save()
        wiz.process()
        self.assertEqual(pick.state, "done")

    def test_bicycode_required_on_product_with_bicycode_greater_amount(self):
        self.picking_type.bicycode_required = True
        self.product_a.has_bicycode = True

        self.so.action_confirm()
        pick = self.so.picking_ids
        pick.move_lines.write({"quantity_done": 3})
        pick.move_line_ids[0].bicycode_ids = [
            (0, 0, {"name": "bicycode_%d" % i}) for i in range(4)
        ]
        wiz_act = pick.button_validate()
        wiz = Form(
            self.env[wiz_act["res_model"]].with_context(wiz_act["context"])
        ).save()
        with self.assertRaisesRegex(
            UserError, "You have set too many bicycodes for product product_a"
        ):
            wiz.process()

    def test_bicycode_get_aggregated_product_quantities(self):
        self.picking_type.bicycode_required = True
        self.product_a.has_bicycode = True

        self.so.action_confirm()
        pick = self.so.picking_ids
        pick.move_lines.write({"quantity_done": 3})
        pick.move_line_ids[0].bicycode_ids = [
            (0, 0, {"name": "bicycode_%d" % i}) for i in range(3)
        ]
        wiz_act = pick.button_validate()
        wiz = Form(
            self.env[wiz_act["res_model"]].with_context(wiz_act["context"])
        ).save()
        wiz.process()
        agg_lines = pick.move_line_ids._get_aggregated_product_quantities()
        self.assertEqual(len(agg_lines), 2)
        expected_line_product_keys = [
            f"{p.id}_{p.name}uom {p.uom_id.id}"
            for p in (self.product_a, self.product_b)
        ]
        self.assertEqual(list(agg_lines.keys()), expected_line_product_keys)
        self.assertEqual(
            agg_lines[expected_line_product_keys[0]]["bicycode_done_values"],
            {"bicycode_%d" % i for i in range(3)},
        )
        self.assertEqual(
            agg_lines[expected_line_product_keys[1]]["bicycode_done_values"], set()
        )
