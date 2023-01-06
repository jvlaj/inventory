from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre


def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # all() is implied by default
    num_authors = Author.objects.count()

    num_skull = Book.objects.filter(title__contains='skul').count()
    num_fiction = Genre.objects.filter(book__genre__name__contains='fiction').count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_fiction': num_fiction,
        'num_skull': num_skull,
    }

    return render(request, 'index.html', context)
