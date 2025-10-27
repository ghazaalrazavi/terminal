import argparse
from model import Passenger, SuperUser, Ticket, Trip
from main import Service
from db import MyContextManager
from dotenv import load_dotenv
import os

load_dotenv()
dsn = os.getenv("DSN")

service = Service("Ticket Service CLI", {}, dsn)

parser = argparse.ArgumentParser(description="Ticket Service Automation CLI")
parser.add_argument(
    "--create-tables", action="store_true", help="Create database tables"
)
parser.add_argument(
    "--register-user",
    nargs=3,
    metavar=("EMAIL", "USERNAME", "PASSWORD"),
    help="Register a traveller",
)
parser.add_argument(
    "--register-admin",
    nargs=3,
    metavar=("EMAIL", "USERNAME", "PASSWORD"),
    help="Register an admin",
)
parser.add_argument(
    "--add-ticket",
    nargs=5,
    metavar=("START", "END", "ORIGIN", "DEST", "COST"),
    help="Add a ticket directly",
)
parser.add_argument("--show-tickets", action="store_true", help="Show all tickets")

args = parser.parse_args()


if args.create_tables:
    service.create_tables()


if args.register_user:
    email, username, password = args.register_user
    user = Passenger(email, username, password)
    service.current_user = user
    with MyContextManager(service.data) as cur:
        cur.execute(
            """
            INSERT INTO users (username, email, wallet)
            VALUES (%s, %s, 0)
            ON CONFLICT (email) DO NOTHING;
        """,
            (username, email),
        )
    print(f"Traveller '{username}' registered successfully.")


if args.register_admin:
    email, username, password = args.register_admin
    admin = SuperUser(email, username, password)
    service.current_user = admin
    with MyContextManager(service.data) as cur:
        cur.execute(
            """
            INSERT INTO users (username, email)
            VALUES (%s, %s)
            ON CONFLICT (email) DO NOTHING;
        """,
            (username, email),
        )
    print(f"Admin '{username}' registered successfully.")


if args.add_ticket:
    start, end, origin, dest, cost = args.add_ticket
    cost = float(cost)
    trip = Trip(start, end, origin, dest)
    ticket = Ticket(trip, cost, 1)
    service.tickets.append(ticket)
    with MyContextManager(service.data) as cur:

        cur.execute(
            """
            INSERT INTO journey (start, end_date, origin, destination)
            VALUES (%s, %s, %s, %s) RETURNING id;
        """,
            (start, end, origin, dest),
        )
        trip_id = cur.fetchone()[0]

        cur.execute(
            """
            INSERT INTO ticket (journey_id, price, quantity)
            VALUES (%s, %s, %s);
        """,
            (trip_id, cost, 1),
        )
    print(f"Ticket added: {origin} → {dest} | {cost}$")


if args.show_tickets:
    service.show_tickets()
# python3 args_parser_view.py --create-tables --register-admin admin@example.com admin AdminPass123! --add-ticket 2025-11-01 2025-11-05 Tehran Shiraz 120 --show-tickets