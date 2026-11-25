"""本轮全部行为测试：只使用 Python 标准库。

选定契约：新账户余额为 0；add/spend 成功后返回 None。
非 int（包括 bool）抛 TypeError，非正整数及余额不足抛 ValueError。
所有被拒绝的操作均保持原余额；不要求具体异常文案。
"""

import unittest

from points_account import PointsAccount


class PointsAccountTests(unittest.TestCase):
    def test_new_account_has_zero_balance(self):
        self.assertEqual(PointsAccount().balance, 0)

    def test_accounts_have_independent_balances(self):
        first = PointsAccount()
        second = PointsAccount()

        first.add(5)

        self.assertEqual(first.balance, 5)
        self.assertEqual(second.balance, 0)

    def test_add_accepts_positive_integers(self):
        for points in (1, 2, 10**30):
            with self.subTest(points=points):
                account = PointsAccount()

                result = account.add(points)

                self.assertEqual(account.balance, points)
                self.assertIsNone(result)

    def test_add_accumulates_points(self):
        account = PointsAccount()

        account.add(3)
        account.add(7)

        self.assertEqual(account.balance, 10)

    def test_spend_subtracts_positive_points(self):
        account = PointsAccount()
        account.add(10)

        result = account.spend(3)

        self.assertEqual(account.balance, 7)
        self.assertIsNone(result)

    def test_spend_can_use_entire_balance(self):
        account = PointsAccount()
        account.add(1)

        account.spend(1)

        self.assertEqual(account.balance, 0)

    def test_add_and_spend_can_be_repeated(self):
        account = PointsAccount()

        account.add(10)
        account.spend(4)
        account.add(2)
        account.spend(3)

        self.assertEqual(account.balance, 5)

    def test_spend_from_empty_account_is_rejected(self):
        account = PointsAccount()

        with self.assertRaises(ValueError):
            account.spend(1)

        self.assertEqual(account.balance, 0)

    def test_insufficient_balance_is_preserved_and_account_remains_usable(self):
        account = PointsAccount()
        account.add(5)

        with self.assertRaises(ValueError):
            account.spend(6)

        self.assertEqual(account.balance, 5)
        account.spend(4)
        self.assertEqual(account.balance, 1)

    def test_add_rejects_nonpositive_integers_without_changing_balance(self):
        for points in (0, -1, -10):
            with self.subTest(points=points):
                account = PointsAccount()
                account.add(5)

                with self.assertRaises(ValueError):
                    account.add(points)

                self.assertEqual(account.balance, 5)

    def test_spend_rejects_nonpositive_integers_without_changing_balance(self):
        for points in (0, -1, -10):
            with self.subTest(points=points):
                account = PointsAccount()
                account.add(5)

                with self.assertRaises(ValueError):
                    account.spend(points)

                self.assertEqual(account.balance, 5)

    def test_add_rejects_nonintegers_without_changing_balance(self):
        for points in (True, False, 1.0, 1.5, "1", None):
            with self.subTest(points=points):
                account = PointsAccount()
                account.add(5)

                with self.assertRaises(TypeError):
                    account.add(points)

                self.assertEqual(account.balance, 5)

    def test_spend_rejects_nonintegers_without_changing_balance(self):
        for points in (True, False, 1.0, 1.5, "1", None):
            with self.subTest(points=points):
                account = PointsAccount()
                account.add(5)

                with self.assertRaises(TypeError):
                    account.spend(points)

                self.assertEqual(account.balance, 5)


if __name__ == "__main__":
    unittest.main()
