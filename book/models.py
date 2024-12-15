from django.db import models
from .consts import MAX_RATE

RATE_CHOICES = [(i, str(i)) for i in range(1, MAX_RATE + 1)]

# class SampleModel(models.Model):
#     title = models.CharField(max_length=100)
#     number = models.IntegerField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

CATEGORY = (('business', 'ビジネス') , ('life', '生活'), ('other', 'その他'))

class Book(models.Model):
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=100, choices=CATEGORY)
    text = models.TextField(blank=True, null=True)
    thumbnail = models.ImageField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

# class Meta:
#     verbose_name = '本のデータ'

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    text = models.TextField()
    rate = models.IntegerField(choices=RATE_CHOICES)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title