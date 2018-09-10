from django.urls import path
from catalog import views


urlpatterns = [
    path('', views.index, name='index'), # this is implemented as function
    path('books', views.BookListView.as_view(), name='books'), # this is implemented as class
    # as_view() does all the work of creating an instance of the class, and making sure that the right handler methods
    # are called for incoming HTTP requests.
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'), #'<int:pk>'  to capture the book id,
    # which must be a specially formatted string, and pass it to the view as a parameter named pk (short for primary
    # key). This is the id that is being used to store the book uniquely in the database, as defined in the Book Model.
    path('authors', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('allbooks/', views.AllLoanedBooksView.as_view(), name='all-borrowed'),
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),

]