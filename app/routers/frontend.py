from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from .books import get_all_books
from ..data.db import SessionDep
from sqlmodel import select
from ..models.book import Book


router = APIRouter() # Parte dal root principale, quindi non mettiamo i prefix

templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse, tags=["HTML Responses"])
def home(request: Request): # Aggiungiamo il parametro alla funzione in modo che la funzione riceva la richiesta http
    '''Returns the home page.'''

    context = {'title': "Welcome to the library"}
    # Se al posto della stringa metto dei tag HTML, questi vengono convertiti in stringa e non vengono interpretati come tag.
    # Ciò che avviene si chiama "escaping". Avviene perché se non fosse così, basterebbe usare i tag script ed eseguire codice arbitrario.
    # L'escaping è attivato di base su Jinja2, nel caso si voglia rendere esplicito, basterà mettere nell'HTML la variabile con l'or
    # Ad esempio {{text|e}}. E' consigliato fare l'operazione esplicita quando si ottengono input dall'esterno.

    context_dict = {'title': "Welcome to the library",
                    'content' : "Hello!"}

    #Se invece mandiamo un dizionario, il dizionario viene convertito in stringa.


    # Ovviamente lavorare con python in stringhe è abominevole, quindi si restituiscono i file HTML nella cartella templates.
    return templates.TemplateResponse(
        name = "home.html", request =request, #Sarà jinja2 ad occuparsi di estendere i blocchi
        context = {"text": context_dict} #Serve a passare i parametri per essere renderizzati sull'HTML | Context prende un dizionario avente come chiavi i nomi delle variabili
    )

@router.get("/book_list", response_class=HTMLResponse, tags=["HTML Responses"])
def show_book_list(request: Request, session: SessionDep):
    books = session.exec(select(Book)).all()
    '''Returns the book list page.'''

    context = books
    #context = get_all_books(session)
    return templates.TemplateResponse(
        name="list.html", request =request,
        context={"books": context}
    )


@router.get("/add_book", response_class=HTMLResponse)
def add_book_form(request: Request):
    '''Returns the add book form.'''
    return templates.TemplateResponse(
        request=request, name="add.html"
    )