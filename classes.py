from validate import *
from pprint import pprint

class User:
    def __init__(self, email, username, password):
        self.email = validate_email(email)
        self.username = validate_username(username)
        self.password = validate_password(password)


class Trip:
    def __init__(self, start, end, status="pending"):
        self.start = start
        self.end = end
        self.status = status

    def change_status(self, status):
        if status not in ("canceled", "done", "pending"):
            raise ValueError("you can only choose between pending,done and canceled")
        self.status = status

    def __str__(self):
        return f"{self.start} => {self.end} | Status: {self.status}"


class Ticket:
    def __init__(self, trip: Trip, cost):
        self.trip = trip
        self.cost = cost

    def __str__(self):
        return f"trip: {self.trip} | Cost: {self.cost}$"


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
        self.__wallet = wallet

    @property 
    def wallet(self):
        return self.__wallet
    
    def charge_wallet(self,amount):
        try:
            if amount < 0:
                raise NegativeValue("amount can not be less than zero")
            self.__wallet+=amount
            print(f"{amount}$ added to youe wallet and your new balance is: {self.__wallet} ")
        except NegativeValue as e:
            print(f'error: {e}')
        
    def history(self,user:Passenger):
        for trip in user.tickets:
            pprint(trip)
    