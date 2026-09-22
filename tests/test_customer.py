from movie_rental.customer import Customer
from movie_rental.movie import Movie
from movie_rental.rental import Rental


def test_statement():
    customer = Customer("Alice")
    customer.add_rental(Rental(Movie("Casablanca", Movie.REGULAR), 3))
    customer.add_rental(Rental(Movie("Dune", Movie.NEW_RELEASE), 2))
    customer.add_rental(Rental(Movie("Frozen", Movie.CHILDRENS), 4))

    assert customer.statement() == (
        "Rental Record for Alice\n"
        "\tCasablanca\t3.5\n"
        "\tDune\t6.0\n"
        "\tFrozen\t3.0\n"
        "Amount owed is 12.5\n"
        "You earned 4 frequent renter points"
    )
