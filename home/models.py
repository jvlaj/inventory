import uuid

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date


class Genre(models.Model):
    name = models.CharField(max_length=200, help_text="Enter a book genre (e.g. Science Fiction)")

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)

    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)

    isbn = models.CharField('ISBN', max_length=13, unique=True,
                            help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')

    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'


class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Unique ID for this particular book across whole library")
    book = models.ForeignKey(Book, on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=20)
    due_back = models.DateField(null=True, blank=True)

    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability',
    )

    def is_overdue(self):
        return bool(self.due_back and date.today() > self.due_back)

    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        return f'{self.id} ({self.book.title})'


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'

# class MyModelName(models.Model):
#     my_field_name = models.CharField(max_length=20, help_text="Enter field documentation", verbose_name="My field name",
#                                      default="char")
#
#     def get_absolute_url(self):
#         return reverse('model-detail-view', args=[str(self.id)])
#
#     def __str__(self):
#         return self.my_field_name
#
#     class Meta:
#         ordering = ['-my_field_name']
#
#     class YearInSchool(models.TextChoices):
#         FRESHMAN = 'FR', _('Freshman')
#         SOPHOMORE = 'SO', _('Sophomore')
#
#     year_in_school = models.CharField(
#         max_length=2,
#         choices=YearInSchool.choices,
#         default=YearInSchool.FRESHMAN
#     )
#
#
# record = MyModelName(my_field_name="Instance #1")
# record.save()
# print(record.id, record.my_field_name)