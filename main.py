from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel, Field
import pdb

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    
    def __init__(self, id, title, author, description, rating):
        """
        Create a new Book with the given id, title, author, description and rating
        :param id: book id
        :param title: book title
        :param author: book author
        :param description: book description
        :param rating: book rating
        """
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating

BOOKS = [
    Book(1, "Title 1", "Author 1", "Description 1", 5),
    Book(2, "Title 2", "Author 2", "Description 2", 4),
    Book(3, "Title 3", "Author 3", "Description 3", 2),
    Book(4, "Title 4", "Author 4", "Description 4", 6),
    Book(5, "Title 5", "Author 5", "Description 5",3),
    Book(6, "Title 6", "Author 6", "Description 6", 6),
    Book(7, "Title7", "Author 7", "Description 7", 6),
    Book(8, "Title 8", "Author 8", "Description 8", 4),
    Book(9, "Title 9", "Author 9", "Description 9", 3),
    Book(10, "Title 10", "Author 10", "Description 10", 2),
    Book(11, "Title 11", "Author 11", "Description 11", 1),
]
    
class BookRequest(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=1, max_length=100)
    author: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(ge=1, le=5)
    
    

@app.get("/books/fetch/all")
async def read_all_books():
    """
    Fetch all books
    
    Returns:
        list: List of all books
    """
    return BOOKS


@app.post("/book/create")
async def create_book(book_request: BookRequest):
    """
    Create a new book with the provided details
    
    Args:
        book_request (pydantic model): Book details
    
    Returns:
        None
    """    
    new_book  = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))
    
    
def find_book_id(book: Book):
    """
    Find the id of a book in the list of books or assign a new one.

    Args:
        book (Book): Book to find the id for

    Returns:
        Book: Book with an id
    """    
    if len(BOOKS) > 0:
        book.id = BOOKS[-1].id + 1
    else:
        book.id = 1
    return book