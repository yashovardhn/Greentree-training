from django.core.management.base import BaseCommand
from django.utils import timezone
from store.models import Book

class Command(BaseCommand):
    help = 'Load sample books into the database'

    def handle(self, *args, **options):
        books = [
            {
                'title': 'The Great Gatsby',
                'author': 'F. Scott Fitzgerald',
                'published_date': '1925-04-10'
            },
            {
                'title': 'To Kill a Mockingbird',
                'author': 'Harper Lee',
                'published_date': '1960-07-11'
            },
            {
                'title': '1984',
                'author': 'George Orwell',
                'published_date': '1949-06-08'
            },
            {
                'title': 'Pride and Prejudice',
                'author': 'Jane Austen',
                'published_date': '1813-01-28'
            },
            {
                'title': 'The Hobbit',
                'author': 'J.R.R. Tolkien',
                'published_date': '1937-09-21'
            }
        ]

        for book_data in books:
            book, created = Book.objects.get_or_create(
                title=book_data['title'],
                defaults={
                    'author': book_data['author'],
                    'published_date': book_data['published_date']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created book: {book.title}'))
            else:
                self.stdout.write(f'Book already exists: {book.title}')
