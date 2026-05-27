# Yelp Database Application

A Python CLI application for querying and interacting with a Yelp-style business dataset stored in a SQL Server database. Supports composable business search with up to four simultaneous filters, user discovery, friend connections, and star-rated reviews.

Built for CMPT-354 (Database Systems) at Simon Fraser University. Grade: A.

---

## Features

- **Business search** — filter by min/max stars, city name, and business name in any combination (up to 4 filters at once)
- **User search** — find users by name, or filter by useful/funny/cool rating attributes
- **Friendship management** — record new friendships between users (with duplicate detection)
- **Review submission** — submit a star rating (1–5) for any business, with auto-generated review ID and timestamp
- **Full input validation** — every prompt re-asks on invalid input; no crashes from bad data

---

## Setup

**Requirements:** Python 3.9+, `pyodbc`, access to the SFU CSIL SQL Server

```bash
git clone https://github.com/arvinbm/Yelp_Database_Application.git
cd Yelp_Database_Application

pip install pyodbc
python3 Assignment7.py
```

> **Note:** The app connects to SFU's `cypress.csil.sfu.ca` SQL Server. You'll need to be on the SFU network (or VPN) and update the connection string in `Assignment7.py` with valid credentials.

---

## Usage

**Login:** Enter a valid user ID from the `user_yelp` table. The program validates the ID before proceeding.

**Main menu:**

```
1. Search a Business
2. Search a User
3. Make a Friend
4. Write a Review
5. Quit the program
```

### Search a Business

Select any combination of filters — the app builds and executes the appropriate SQL query:

| Filter | Description |
|---|---|
| Min stars | Businesses with the lowest star rating in the dataset |
| Max stars | Businesses with the highest star rating in the dataset |
| City | Case-insensitive city name match |
| Name | Partial name match (`LIKE %query%`) |

Results are ordered by business name.

### Search a User

Filter users by name (partial match) and/or one or more attributes — `useful > 0`, `funny > 0`, `cool > 0`. Results are ordered by name.

### Make a Friend

Enter a user ID to record a friendship. Validates that the ID exists and that the friendship isn't already in the database before inserting.

### Write a Review

Enter a business ID and a star rating (1–5). The app generates a unique 22-character alphanumeric review ID, checks for collisions, then inserts the review with the current timestamp.

---

## Project Structure

```
Yelp_Database_Application/
└── Assignment7.py    # Full application — login, menu, all CRUD and query logic
```

---

## Tech Stack

| Layer | Technologies |
|---|---|
| Language | Python 3 |
| Database | Microsoft SQL Server (SFU CSIL cluster) |
| Connectivity | `pyodbc` (ODBC Driver 18 for SQL Server) |
| Query design | Parameterized SQL with indexed lookups on `name`, `city`, `stars` |
