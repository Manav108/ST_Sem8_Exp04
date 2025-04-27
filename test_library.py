import pytest
from library import Library, BookAlreadyExists, BookNotAvailable, InvalidUser

@pytest.fixture
def library():
    lib = Library()
    lib.add_book("The Alchemist", 3)
    lib.add_book("1984", 2)
    lib.register_user("alice")
    lib.register_user("bob")
    return lib

def test_add_book_success():
    lib = Library()
    lib.add_book("New Book", 4)
    assert lib.books["New Book"] == 4

def test_add_duplicate_book(library):
    with pytest.raises(BookAlreadyExists):
        library.add_book("1984", 1)

def test_add_book_invalid_copies():
    lib = Library()
    with pytest.raises(ValueError):
        lib.add_book("Zero Copies Book", 0)

def test_remove_book_success(library):
    library.remove_book("1984")
    assert "1984" not in library.books

def test_remove_nonexistent_book(library):
    with pytest.raises(BookNotAvailable):
        library.remove_book("Unknown Book")

def test_register_user_success():
    lib = Library()
    lib.register_user("charlie")
    assert "charlie" in lib.users

def test_register_duplicate_user(library):
    with pytest.raises(InvalidUser):
        library.register_user("alice")

def test_unregister_user_success(library):
    library.unregister_user("alice")
    assert "alice" not in library.users

def test_unregister_nonexistent_user(library):
    with pytest.raises(InvalidUser):
        library.unregister_user("unknown_user")

def test_borrow_book_success(library):
    library.borrow_book("alice", "The Alchemist")
    assert "The Alchemist" in library.borrowed_books["alice"]
    assert library.books["The Alchemist"] == 2

def test_borrow_book_unregistered_user(library):
    with pytest.raises(InvalidUser):
        library.borrow_book("unknown", "1984")

def test_borrow_book_not_available(library):
    library.borrow_book("alice", "1984")
    library.borrow_book("bob", "1984")
    with pytest.raises(BookNotAvailable):
        library.borrow_book("alice", "1984")

def test_return_book_success(library):
    library.borrow_book("alice", "1984")
    library.return_book("alice", "1984")
    assert "1984" not in library.borrowed_books["alice"]
    assert library.books["1984"] == 2

def test_return_book_user_not_registered(library):
    with pytest.raises(InvalidUser):
        library.return_book("unknown", "1984")

def test_return_book_not_borrowed(library):
    with pytest.raises(BookNotAvailable):
        library.return_book("alice", "1984")

def test_available_books(library):
    available = library.available_books()
    assert "The Alchemist" in available
    assert available["The Alchemist"] == 3

def test_user_borrowed_books(library):
    library.borrow_book("bob", "The Alchemist")
    borrowed = library.user_borrowed_books("bob")
    assert "The Alchemist" in borrowed

def test_user_borrowed_books_invalid_user(library):
    with pytest.raises(InvalidUser):
        library.user_borrowed_books("ghost")

def test_total_books_count(library):
    assert library.total_books_count() == 5  # 3 + 2 initially
    library.borrow_book("alice", "The Alchemist")
    assert library.total_books_count() == 4  # One less after borrowing
