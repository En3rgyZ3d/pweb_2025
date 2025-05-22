from fastapi import APIRouter

from ..models.book import Book, BookPublic
from ..models.user import User,UserPublic
from ..models.book_user_link import BookUserLink
from ..data.db import SessionDep

from sqlmodel import select


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
def get_all_users(session:SessionDep) -> list[UserPublic]:
    '''Returns all users.'''
    statement = select(User)
    users = session.exec(statement).all()
    return users


@router.get("/{id}/books")
def get_user_books(session:SessionDep, id:int) -> list[BookPublic]:
    '''Returns all books held by the given user.'''
    statement = select(Book).join(BookUserLink).where(BookUserLink.user_id == id) # NOQA | Warning ignorabile, bug non risolto sui check dei type
    books = session.exec(statement).all()
    return books



