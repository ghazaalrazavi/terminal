import pytest
from model import Trip,Ticket,SuperUser,Dashboard,Passenger
from validate import *


# Trip tests
def test_trip_creation():
    trip = Trip("2025-01-01", "2025-01-02", "Tehran", "Mashhad")
    assert trip.start == "2025-01-01"
    assert trip.end == "2025-01-02"
    assert trip.origin == "Tehran"
    assert trip.destination == "Mashhad"
    assert trip.status == "pending"

def test_change_status_valid():
    trip = Trip("2025-01-01", "2025-01-02")
    trip.change_status("done")
    assert trip.status == "done"

def test_change_status_invalid():
    trip = Trip("2025-01-01", "2025-01-02")
    with pytest.raises(ValueError):
        trip.change_status("unknown")


@pytest.fixture
def sample_ticket():
    trip = Trip("2025-01-01", "2025-01-02", "Tehran", "Mashhad")
    return Ticket(trip, 100, 2)

def test_reserve_ticket(sample_ticket):
    sample_ticket.reserve()
    assert sample_ticket.status == "reserved"
    assert sample_ticket.quantity == 1

def test_reserve_ticket_twice_error(sample_ticket):
    sample_ticket.reserve()
    with pytest.raises(TripStarted):
        sample_ticket.reserve()

def test_confirm_ticket(sample_ticket):
    sample_ticket.reserve()
    sample_ticket.confirm()
    assert sample_ticket.status == "paid"

def test_confirm_without_reserve(sample_ticket):
    with pytest.raises(TripStarted):
        sample_ticket.confirm()

def test_cancel_reservation(sample_ticket):
    sample_ticket.reserve()
    sample_ticket.cancel_reservation()
    assert sample_ticket.status == "canceled"
    assert sample_ticket.quantity == 2


def test_passenger_get_ticket():
    passenger = Passenger("passenger@example.com", "Alice", "Aa123456!")
    ticket = Ticket(Trip("2025-01-01", "2025-01-02"), 100)
    passenger.get_ticket(ticket)
    assert ticket in passenger.tickets

def test_passenger_get_ticket_invalid_type():
    passenger = Passenger("passenger@example.com", "Alice", "Aa123456!")
    with pytest.raises(TypeError):
        passenger.get_ticket("not_a_ticket")


def test_superuser_creation():
    su = SuperUser("admin@example.com", "Admin", "Aa123456!")
    assert su.email == "admin@example.com"
    assert su.username == "Admin"
    assert su.password == "Aa123456!"


def test_dashboard_history_print(capsys):
    passenger = Passenger("passenger@example.com", "Alice", "Aa123456!")
    ticket = Ticket(Trip("2025-01-01", "2025-01-02", "Tehran", "Mashhad"), 100)
    passenger.get_ticket(ticket)
    dashboard = Dashboard(passenger, 50)
    dashboard.history()
    captured = capsys.readouterr()
    assert "Ticket history:" in captured.out
    assert "Tehran → Mashhad" in captured.out
