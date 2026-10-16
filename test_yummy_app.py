import unittest
from unittest.mock import patch

import gps_service
from yummy_app import YummyApp


class TestEasyLevel(unittest.TestCase):
    def setUp(self):
        self.app = YummyApp()

    def test_calculate_total_for_single_item(self):
        self.assertEqual(self.app.calculate_order_total({"pho": 2}), 100000)

    def test_calculate_total_for_multiple_items(self):
        self.assertEqual(
            self.app.calculate_order_total({"pho": 1, "bun": 1}), 95000
        )

    def test_calculate_total_for_empty_cart(self):
        self.assertEqual(self.app.calculate_order_total({}), 0.0)

    def test_calculate_total_with_zero_quantity(self):
        self.assertEqual(self.app.calculate_order_total({"pho": 0}), 0.0)

    def test_unknown_item_is_ignored(self):
        self.assertEqual(self.app.calculate_order_total({"pizza": 2}), 0.0)

    def test_negative_quantity_is_ignored(self):
        self.assertEqual(self.app.calculate_order_total({"pho": -1}), 0.0)


class TestMediumLevel(unittest.TestCase):
    def test_valid_promo_online(self):
        app = YummyApp(network_status="online", os_version=15)
        self.assertAlmostEqual(app.apply_promo_code(100000, "GIAM10"), 90000)

    def test_promo_offline_raises_connection_error(self):
        app = YummyApp(network_status="offline")
        with self.assertRaisesRegex(ConnectionError, "Khong co ket noi mang"):
            app.apply_promo_code(100000, "GIAM10")

    def test_special_promo_on_os15(self):
        app = YummyApp(os_version=15)
        self.assertAlmostEqual(app.apply_promo_code(100000, "NEW_OS_ONLY"), 80000)

    def test_special_promo_on_os14_raises_value_error(self):
        app = YummyApp(os_version=14)
        with self.assertRaisesRegex(ValueError, "HDH phien ban 15"):
            app.apply_promo_code(100000, "NEW_OS_ONLY")

    def test_invalid_promo_raises_value_error(self):
        with self.assertRaisesRegex(ValueError, "Ma khuyen mai khong hop le"):
            YummyApp().apply_promo_code(100000, "INVALID")


class TestHardLevel(unittest.TestCase):
    @patch("yummy_app.gps_service.get_current_location")
    def test_gps_inside_service_area(self, mock_gps):
        mock_gps.return_value = (10.0, 105.0)
        self.assertEqual(
            YummyApp().get_nearby_restaurants(),
            ["Nha hang Pho Ly Quoc Su", "Bun cha Huong Lien"],
        )
        mock_gps.assert_called_once_with()

    @patch("yummy_app.gps_service.get_current_location")
    def test_gps_outside_service_area(self, mock_gps):
        mock_gps.return_value = (20.0, 110.0)
        self.assertEqual(YummyApp().get_nearby_restaurants(), [])
        mock_gps.assert_called_once_with()

    @patch("yummy_app.gps_service.get_current_location")
    def test_gps_signal_lost(self, mock_gps):
        mock_gps.side_effect = gps_service.GPSSignalLostError("Lost signal")
        self.assertEqual(
            YummyApp().get_nearby_restaurants(), "Khong the xac dinh vi tri."
        )
        mock_gps.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
