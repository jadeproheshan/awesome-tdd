"""Small in-memory room booking module; times are integer minutes."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Reservation:
    id: int
    room: str
    start: int
    end: int


class BookingConflict(ValueError):
    """The room is already booked for an overlapping interval."""


class BookingBook:
    def __init__(self):
        self._reservations = {}
        self._next_id = 1

    def create(self, room: str, start: int, end: int) -> Reservation:
        if type(start) is not int or type(end) is not int:
            raise TypeError("start and end must be integer minutes")
        if start >= end:
            raise ValueError("start must be before end")
        for existing in self._reservations.values():
            if existing.room == room and start < existing.end and existing.start < end:
                raise BookingConflict("room is already booked for that interval")
        reservation = Reservation(self._next_id, room, start, end)
        self._reservations[reservation.id] = reservation
        self._next_id += 1
        return reservation

    def cancel(self, reservation_id: int) -> None:
        """Cancel an existing reservation; raise KeyError for an unknown ID."""
        del self._reservations[reservation_id]
