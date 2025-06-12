from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    """Автор"""
    surname = models.CharField("Фамилия", max_length=50)
    first_name = models.CharField("Имя", max_length=50)
    last_name = models.CharField("Отчество", max_length=50, blank=True)
    birth_year = models.IntegerField("Год рождения", validators=[
            MinValueValidator(1000),
            MaxValueValidator(2000),
        ])

    def __str__(self):
        return self.surname + ' ' + self.first_name + ' ' + self.last_name

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"

class Book(models.Model):
    """Книга"""
    title = models.CharField("Название", max_length=200, unique=True)
    description = models.TextField("Описание", max_length=3000)
    cover_image = models.CharField("Обложка", max_length=100, unique=True)
    page_number = models.IntegerField("Объем", validators=[
            MinValueValidator(1),
            MaxValueValidator(1500),
        ])
    authors = models.ManyToManyField(Author, verbose_name="Авторы")
    genre = models.CharField("Жанр", max_length=30)
    link = models.CharField("Ссылка на скачивание", max_length=100, unique=True)
    year = models.IntegerField("Год", validators=[
            MinValueValidator(1000),
            MaxValueValidator(2040),
        ])

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"

class Review(models.Model):
    """Отзыв на книгу"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey("Book", on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField(validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ])
    created_at = models.DateTimeField(auto_now_add=True)

class Order(models.Model):
    """Заказ книги"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=100)
    book = models.ForeignKey("Book", on_delete=models.CASCADE)
    ordered_at = models.DateTimeField(auto_now_add=True)

class Feedback(models.Model):
    """Обратная связь"""
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=70)
    subject = models.CharField(max_length=70)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
