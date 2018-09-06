from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
# Create your views here.

def index(request):
    """View for the Homepage"""

    # Count books
    book_nr = Book.objects.all().count()
    # Count instances of books
    bookinst_nr = BookInstance.objects.all().count()
    # Nr of available books
    av_books = BookInstance.objects.filter(status__exact = 'a').count()
    # Nr of Authors
    author_nr = Author.objects.count()

    # Count of genre and count of books containing a word
    # cw_books = Book.objects.filter(title__icontains = 'and').count()
    # cw_genre = Book.objects.filter(genre__name__icontains = 'fIction').count() #Needed __name because genre is a ManyToMany mapping

    context = {
        'book_nr': book_nr,
        'bookinst_nr': bookinst_nr,
        'av_books': av_books,
        'author_nr': author_nr,
        # 'cw_books': cw_books,
        # 'cw_genre': cw_genre,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)
