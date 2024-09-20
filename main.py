import datetime
from typing import Optional
from fastapi import FastAPI, Path, Query
from pydantic import BaseModel, Field, field_validator
import pdb
import re

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published: str
    
    def __init__(self, id, title, author, description, rating, published):
        """
        Create a new Book with the given id, title, author, description and rating
        :param id: book id
        :param title: book title
        :param author: book author
        :param description: book description
        :param rating: book rating
        :param published: book publication date
        """
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published = published

BOOKS = [
    Book(1, "Title 1", "Author 1", "Description 1", 5, "2020-01-01"),
    Book(2, "Title 2", "Author 2", "Description 2", 4, "2020-02-01"),
    Book(3, "Title 3", "Author 3", "Description 3", 2, "2020-03-01"),
    Book(4, "Title 4", "Author 4", "Description 4", 6, "2020-04-01"),
    Book(5, "Title 5", "Author 5", "Description 5", 3, "2020-05-01"),
    Book(6, "Title 6", "Author 6", "Description 6", 6, "2020-06-01"),
    Book(7, "Title7", "Author 7",  "Description 7", 5, "2020-06-01"),
    Book(8, "Title 8", "Author 8", "Description 8", 4, "2020-08-01"),
    Book(9, "Title 9", "Author 9", "Description 9", 3, "2020-01-01"),
    Book(10, "Title 10", "Author 10", "Description 10", 2, "2020-03-01"),
    Book(11, "Title 11", "Author 11", "Description 11", 1, "2020-06-01"),
]
    
class BookRequest(BaseModel):
    id: Optional[int] = Field(description="Id is not required", default=None)
    title: str = Field(min_length=1, max_length=100)
    author: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(ge=1, le=5)
    published: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Title of the Book",
                "author": "Name of the Author",
                "description": "Description of the Book",
                "rating": 5,
                "published": "YYYY-MM-DD"
            }
        }
    }
    
    @field_validator('published')
    @classmethod
    def published_validator(cls, published_date: str)-> str:
        try:
            datetime.strptime(published_date, '%Y-%m-%d')
        except ValueError:
            raise ValueError('Published date should be in YYYY-MM-DD format')
        return published_date
    

@app.get("/books/fetch/all")
async def read_all_books():
    """
    Fetch all books
    
    Returns:
        list: List of all books
    """
    return BOOKS

@app.get("/books/fetch/{book_id}")
async def read_book(book_id: int = Path(gt=0)):
    """
    Fetch a book with the given id
    
    Args:
        book_id (int): Id of the book to fetch
    
    Returns:
        Book: Book with the given id
    """    
    for book in BOOKS:
        if book.id == book_id:
            return book
        
@app.get("/books/fetch/rating/{rating}")
async def read_book_by_rating(rating: int = Path(gt=0)):
    """
    Fetch a book with the given rating
    
    Args:
        rating (int): Rating of the book
    
    Returns:
        list: List of books with the given rating
    """    
    books_to_return = []
    for book in BOOKS:
        if book.rating == rating:
            books_to_return.append(book)
    return books_to_return


@app.get("/books/fetch")
async def read_book_by_params(title: Optional[str] = None, author: Optional[str] = None, rating: Optional[int] = 1, 
                               published: Optional[str] = None):
    """
    Fetch a book with the given parameters
    
    Args:
        title (str): Title of the book
        author (str): Author of the book
        rating (int): Rating of the book
    
    Returns:
        list: List of books with the given parameters
    """    
    results = BOOKS
    if title:
        results = [book for book in results if book.title == title]
    if author:
        results = [book for book in results if book.author == author]
    if rating:
        results = [book for book in results if book.rating == rating]
    if published:
        results = [book for book in results if book.published == published]
    return results



@app.post("/books/create")
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


@app.put("/books/update/{book_id}")
async def update_book(book_request: BookRequest, book_id: int = Path(gt=0)):
    """
    Update a book with the provided details
    
    Args:
        book_id (int): Id of the book to update
        book_request (pydantic model): Book details
    
    Returns:
        None
    """    
    for book in BOOKS:
        if book.id == book_id:
            book.title = book_request.title
            book.author = book_request.author
            book.description = book_request.description
            book.rating = book_request.rating
    

@app.delete("/books/delete/{book_id}")
async def delete_book(book_id: int = Path(gt=0)):
    """
    Delete a book with the given id
    
    Args:
        book_id (int): Id of the book to delete
    
    Returns:
        None
    """    
    global BOOKS
    BOOKS = [book for book in BOOKS if book.id != book_id]
    
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