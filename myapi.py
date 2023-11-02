from typing import Optional
from fastapi import FastAPI, Path
from pydantic import BaseModel


class Book(BaseModel):
    title: str
    author: str
    edition: str
    quantity: int


class updateBook(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    edition: Optional[str] = None
    quantity: Optional[int] = None


app = FastAPI()


books = {
    1: {
        "title": "Le pagne noir",
        "author": "Bernard Dadié",
        "edition": "Présence Africaine",
        "quantity": 4,
    },
    2: {
        "title": "La belle et le bête",
        "author": "Charles Perrault",
        "edition": "Claude Barbin",
        "quantity": 1,
    },
    3: {
        "title": "Cendrillon",
        "author": "Charles Perrault",
        "edition": "Claude Barbin",
        "quantity": 7,
    },

}


@app.get("/")
def index():
    return {"name": "First name"}


@app.get("/get-books/")
def get_book():
    return books


@app.get("/get-book/{book_id}")
def get_book(book_id: int = Path(description="The ID of the book to retreive")):
    return books[book_id]


@app.get("/get-by-title")
def get_book(title: str = Path(description="The title of the book to retrieve")):
    for book_id in books:
        if books[book_id]["Title"] == title:
            return books[book_id]


@app.get("/get-by-title-with-id/{book_id}")
def get_book(book_id: int, title: str = Path(description="The title and the id of the book to retrieve")):
    for book_id in books:
        if books[book_id]["Title"] == title:
            return books[book_id]


@app.post("/create-book/")
def create_book(book: Book):
    if book == None:
        return {"Error": "Book not filled"}

    if len(books) == 0:
        books[0] = book
    else:
        last_id = list(books.keys())[-1]
        books[last_id+1] = book
        return book


@app.put("/update-book/{book_id}")
def update_book(book_id: int, book: updateBook):
    if book_id not in books:
        return {"Error": "Book does not exist"}

    if book.title != None:
        books[book_id].title = book.title
    if book.author != None:
        books[book_id].author = book.author
    if book.edition != None:
        books[book_id].edition = book.edition
    if book.quantity != None:
        books[book_id].quantity = book.quantity

    return books[book_id]


@app.delete("/delete-book/{book_id}")
def delete_book(book_id: int):
    if book_id not in books:
        return {"Error": "Book does not exist"}

    del books[book_id]
    return {"Message": "Book deleted successfully"}
