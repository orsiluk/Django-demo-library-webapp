from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin  # Needed to restrict acess to logged in users only
from django.contrib.auth.mixins import PermissionRequiredMixin

# Create your views here.

def index(request):
    """View for the Homepage"""

    # Count books
    book_nr = Book.objects.all().count()
    # Count instances of books
    bookinst_nr = BookInstance.objects.all().count()
    # Nr of available books
    av_books = BookInstance.objects.filter(status__exact='a').count()
    # Nr of Authors
    author_nr = Author.objects.count()

    # Count of genre and count of books containing a word
    # cw_books = Book.objects.filter(title__icontains = 'and').count()
    # cw_genre = Book.objects.filter(genre__name__icontains = 'fIction').count() #Needed_name because genre is a ManyToMany mapping

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'book_nr': book_nr,
        'bookinst_nr': bookinst_nr,
        'av_books': av_books,
        'author_nr': author_nr,
        'num_visits': num_visits,
        # 'cw_books': cw_books,
        # 'cw_genre': cw_genre,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


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
    paginate_by = 10


class AuthorDetailView(generic.DetailView):
    model = Author


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'mybooks'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

class AllLoanedBooksView(PermissionRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_librarian.html'
    paginate_by = 10
    permission_required = 'catalog.can_mark_returned'

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')


# Setting up form submission
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime

from .forms import RenewBookForm

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        book_renewal_form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if book_renewal_form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = book_renewal_form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed'))

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        book_renewal_form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': book_renewal_form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = Author
    fields = '__all__'
    initial={'date_of_death':'05/01/2018',}
    permission_required = 'catalog.can_mark_returned'

class AuthorUpdate(UpdateView, PermissionRequiredMixin):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    permission_required = 'catalog.can_mark_returned'

class AuthorDelete(DeleteView, PermissionRequiredMixin):
    model = Author
    success_url = reverse_lazy('authors')
    permission_required = 'catalog.can_mark_returned'


class BookCreate(CreateView, PermissionRequiredMixin):
    model = Book
    fields = '__all__'
    permission_required = 'catalog.can_mark_returned'

class BookUpdate(UpdateView, PermissionRequiredMixin):
    model = Book
    fields = ['author', 'summary', 'isbn', 'genre', 'language']
    permission_required = 'catalog.can_mark_returned'

class BookDelete(DeleteView, PermissionRequiredMixin):
    model = Book
    success_url = reverse_lazy('books')
    permission_required = 'catalog.can_mark_returned'