from rest_framework import serializers
from ..models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'published_date', 'price']
        read_only_fields = ['id']

    def validate_price(self, value):
        """
        Check that the price is greater than 0.
        """
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0.")
        return value

    def validate_published_date(self, value):
        """
        Check that the published_date is not in the future.
        """
        from django.utils import timezone
        if value > timezone.now().date():
            raise serializers.ValidationError("Published date cannot be in the future.")
        return value
