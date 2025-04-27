class BookNotAvailable(Exception):
    pass

class BookAlreadyExists(Exception):
    pass

class InvalidUser(Exception):
    pass

class Library:
    def __init__(self):
        self.books = {}  # { title: copies }
        self.users = set()  # registered users
        self.borrowed_books = {}  # { user: [titles] }

    def register_user(self, user):
        if user in self.users:
            raise InvalidUser(f"User '{user}' is already registered.")
        self.users.add(user)
        self.borrowed_books[user] = []

    def unregister_user(self, user):
        if user not in self.users:
            raise InvalidUser(f"User '{user}' not found.")
        self.users.remove(user)
        del self.borrowed_books[user]

    def add_book(self, title, copies=1):
        if title in self.books:
            raise BookAlreadyExists(f"The book '{title}' already exists.")
        if copies <= 0:
            raise ValueError("Number of copies must be positive.")
        self.books[title] = copies

    def remove_book(self, title):
        if title not in self.books:
            raise BookNotAvailable(f"The book '{title}' is not in the library.")
        del self.books[title]

    def borrow_book(self, user, title):
        if user not in self.users:
            raise InvalidUser(f"User '{user}' is not registered.")
        if title not in self.books or self.books[title] == 0:
            raise BookNotAvailable(f"The book '{title}' is not available.")
        self.books[title] -= 1
        self.borrowed_books[user].append(title)

    def return_book(self, user, title):
        if user not in self.users:
            raise InvalidUser(f"User '{user}' is not registered.")
        if title not in self.borrowed_books[user]:
            raise BookNotAvailable(f"User '{user}' did not borrow the book '{title}'.")
        self.books[title] += 1
        self.borrowed_books[user].remove(title)

    def available_books(self):
        return {title: count for title, count in self.books.items() if count > 0}

    def user_borrowed_books(self, user):
        if user not in self.users:
            raise InvalidUser(f"User '{user}' is not registered.")
        return self.borrowed_books[user]

    def total_books_count(self):
        return sum(self.books.values())
