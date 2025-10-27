from validate import *
from pprint import pprint

class User:
    def __init__(self, email, username, password):
        self.email = validate_email(email)
        self.username = validate_username(username)
        self.password = validate_password(password)


class Trip:
    def __init__(self, start, end,origin=None,destination=None ,status="pending"):
        self.start = start
        self.end = end
        self.status = status
        self.origin = origin
        self.destination = destination


    def change_status(self, status):
        if status not in ("canceled", "done", "pending"):
            raise ValueError("you can only choose between pending,done and canceled")
        self.status = status

    def __str__(self):
        return f"{self.start} => {self.end} | Status: {self.status}"


class Ticket:
    def __init__(self, trip: Trip, cost,quantity=1):
        self.trip = trip
        self.cost = cost
        self.quantity = quantity
        self.status = "pending"

    def __str__(self):
        return f"trip: {self.trip} | Cost: {self.cost}$"
    
    def reserve(self):
        if self.status != 'pending':
            raise TripStarted("you can't reserve this ticket")
        if self.quantity <= 0:
            raise ValueError("No tickets left.")
        self.quantity -= 1
        self.status = 'reserved'
        print(" Ticket reserved successfully.")

    def confirm(self):
        if self.status != 'reserved':
            raise TripStarted("Only reserved tickets can be confirmed.")
        self.status = 'paid'
        print(" Ticket payment confirmed.")

    def cancel_reservation(self):
        if self.status not in ('reserved', 'paid'):
            raise TripStarted("Only reserved or paid tickets can be canceled.")
        self.status = 'canceled'
        self.quantity += 1
        print(" Ticket canceled.")
    



class Passenger(User):
    def __init__(self, email, username, password):
        super().__init__(email, username, password)
        self.tickets = []

    def get_ticket(self, ticket: Ticket):
        if isinstance(ticket, Ticket):
            self.tickets.append(ticket)
        else:
            raise TypeError("ticket type is not matched")


class SuperUser(User):
    def __init__(self, email, username, password):
        super().__init__(email, username, password)

class Dashboard():
    def __init__(self,user:Passenger,wallet):
        self.user = user
        self.wallet = wallet
    
    def charge_wallet(self, amount):
        try:
            if amount < 0:
                raise NegativeValue("amount can not be less than zero")
            self.wallet += amount
            from db import MyContextManager
            import os
            dsn = os.getenv("DSN")
            with MyContextManager(dsn) as cur:
                cur.execute("UPDATE users SET wallet = %s WHERE email = %s;", (self.wallet, self.user.email))
            print(f"{amount}$ added to your wallet and your new balance is: {self.wallet}")
        except NegativeValue as e:
            print(f'error: {e}')

    def history(self):
        if not self.user.tickets:
            print("No tickets has been purchased yet.")
        else:
            print("Ticket history:")
            for ticket in self.user.tickets:
                print(ticket)