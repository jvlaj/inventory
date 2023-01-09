from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required


def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # all() is implied by default
    num_authors = Author.objects.count()

    num_skull = Book.objects.filter(title__icontains='skul').count()
    num_fiction = Genre.objects.filter(book__genre__name__icontains='fiction').count()

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_fiction': num_fiction,
        'num_skull': num_skull,
        'num_visits': num_visits,
    }

    return render(request, 'index.html', context)


class BookListView(generic.ListView):
    model = Book
    paginate_by = 10

    # def get_queryset(self, **kwargs):
    #     return Book.objects.filter(title__icontains='war')[:5]

    def get_context_data(self, *, object_list=None, **kwargs):
        # call base implementation with super() to get the context
        context = super(BookListView, self).get_context_data(**kwargs)
        context['some_data'] = 'This is just some data'
        return context


class BookDetailView(generic.DetailView):
    model = Book


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10


class AuthorDetailView(generic.DetailView):
    model = Author


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'home/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o', ).order_by('due_back')


class AllLoanedBooksByListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = BookInstance
    permission_required = 'home.can_mark_returned'
    template_name = 'home/bookinstance_list_all_borrowed.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o', ).order_by('due_back')
