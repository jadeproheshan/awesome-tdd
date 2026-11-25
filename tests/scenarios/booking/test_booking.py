import unittest

from booking import BookingBook, BookingConflict, Reservation


class BookingTests(unittest.TestCase):
    def setUp(self):
        self.book = BookingBook()

    def test_create_returns_reservation(self):
        self.assertEqual(
            Reservation(1, "A", 60, 120), self.book.create("A", 60, 120)
        )

    def test_requires_integer_minutes_and_start_before_end(self):
        for start, end in [(60, 60), (120, 60)]:
            with self.subTest(start=start, end=end):
                with self.assertRaises(ValueError):
                    self.book.create("A", start, end)
        for start, end in [(1.5, 2), (1, "2"), (True, 2), (1, False)]:
            with self.subTest(start=start, end=end):
                with self.assertRaises(TypeError):
                    self.book.create("A", start, end)

    def test_rejects_all_same_room_overlap_shapes(self):
        for start, end in [(60, 120), (30, 90), (90, 150), (70, 110), (30, 150)]:
            with self.subTest(start=start, end=end):
                book = BookingBook()
                book.create("A", 60, 120)
                with self.assertRaises(BookingConflict):
                    book.create("A", start, end)

    def test_allows_adjacent_reservations_in_both_directions(self):
        middle = self.book.create("A", 60, 120)
        before = self.book.create("A", 0, 60)
        after = self.book.create("A", 120, 180)
        self.assertEqual((0, 60), (before.start, before.end))
        self.assertEqual((120, 180), (after.start, after.end))
        self.assertEqual(3, len({middle.id, before.id, after.id}))

    def test_different_rooms_can_overlap(self):
        first = self.book.create("A", 60, 120)
        second = self.book.create("B", 60, 120)
        self.assertEqual(("B", 60, 120), (second.room, second.start, second.end))
        self.assertNotEqual(first.id, second.id)
        with self.assertRaises(BookingConflict):
            self.book.create("B", 90, 100)

    def test_cancel_releases_only_the_selected_reservation(self):
        removed = self.book.create("A", 60, 120)
        retained = self.book.create("A", 120, 180)
        self.book.create("B", 60, 120)
        self.book.cancel(removed.id)
        replacement = self.book.create("A", 60, 120)
        self.assertEqual(("A", 60, 120), (
            replacement.room, replacement.start, replacement.end
        ))
        self.assertNotEqual(removed.id, replacement.id)
        self.assertNotEqual(retained.id, replacement.id)
        with self.assertRaises(BookingConflict):
            self.book.create("A", 150, 160)
        with self.assertRaises(BookingConflict):
            self.book.create("B", 90, 100)


if __name__ == "__main__":
    unittest.main()
