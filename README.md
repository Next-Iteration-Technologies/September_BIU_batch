# Movie Rental

## Problem statement

A video store rents `Movie`s to `Customer`s. Each movie has a price code that
determines how a rental is charged and how many frequent renter points it
earns:

| Price code       | Amount                                              | Frequent renter points          |
|-------------------|------------------------------------------------------|----------------------------------|
| `REGULAR`         | \$2 flat, plus \$1.5/day beyond 2 days                | 1                                |
| `NEW_RELEASE`      | \$3/day rented                                        | 2 if rented more than 1 day, else 1 |
| `CHILDRENS`        | \$1.5 flat, plus \$1.5/day beyond 3 days              | 1                                |

`Customer.statement()` produces a plain-text statement listing each rental,
the total amount owed, and the total frequent renter points earned, e.g.:

```
Rental Record for Alice
	Casablanca	3.5
	Dune	6.0
	Frozen	3.0
Amount owed is 12.5
You earned 4 frequent renter points
```

## Setup

Requires Python 3.12+ and `pytest` (no other dependencies). The package
lives under `src/movie_rental`; a `pyproject.toml` adds `src` to the
pytest path so it can be imported without installing the package.

```
pip install pytest
```

## How to run tests

    python -m pytest
