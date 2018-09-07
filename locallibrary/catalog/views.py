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
    # cw_genre = Book.objects.filter(genre__name__icontains = 'fIction').count() #Needed_name because genre is a ManyToMany mapping

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

from django.views import generic

class BookListView(generic.ListView):
    """That's it! The generic view will query the database to get all records for the specified model (Book) then render
     a template located at /locallibrary/catalog/templates/catalog/book_list.html """
    model = Book
    paginate_by = 10
    # Lots of stuff we can do:
    # context_object_name = 'my_book_list'  # your own name for the list as a template variable
    # queryset = Book.objects.filter(title__icontains='and')[:5]  # Get 5 books containing the title and
    # template_name = 'books/my_arbitrary_template_name_list.html'  # Specify your own template name/location

    # Add to context variables:
    # def get_context_data(self, **kwargs):
    #     # Call the base implementation first to get the context
    #     context = super(BookListView, self).get_context_data(**kwargs)
    #     # Create any data and add it to the context
    #     context['more_data'] = 'Books are pretty cool!'
    #     return context

class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author

class AuthorDetailView(generic.DetailView):
    model = Author