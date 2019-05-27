from django.db import models
from django.contrib.auth.models import User as uu
import datetime

# Media author
class MediaAuthor(models.Model):
    name = models.CharField(max_length=70)
    surname = models.CharField(max_length=70)
    birthday = models.DateField
    img = models.ImageField(upload_to='gallery', default='gallery/no-img.png')

    def __str__(self):
        return self.name + " " + self.surname


class Media(models.Model):
    name = models.CharField(max_length=70)
    date_published = models.DateTimeField(default=datetime.date.today)
    date_added = models.DateTimeField(default=datetime.date.today)

    #Media genre
    ACTION = "Action"
    ADVENTURE = "Adventure"
    DRAMA = "Drama"
    COMEDY = "Comedy"
    SYFY = "SyFy"

    CHOICES = [
        (ACTION, 'Action'),
        (ADVENTURE, 'Adventure'),
        (DRAMA, 'Drama'),
        (COMEDY, 'Comedy'),
        (SYFY, 'SyFy'),
    ]

    mgenre = models.CharField(
        max_length=20,
        choices=CHOICES,
        default=ACTION,
    )

    # Media Type
    MOVIE = 'Movie'
    BOOK = 'Book'
    SERIES = 'Series'

    CHOICES = [
        (MOVIE, 'Movie'),
        (BOOK, 'Book'),
        (SERIES, 'Series'),
    ]

    mtype = models.CharField(
        max_length=20,
        choices=CHOICES,
        default=MOVIE,
    )

    author = models.ForeignKey(MediaAuthor, on_delete=models.CASCADE)
    description = models.CharField(max_length=5000)
    img = models.ImageField(upload_to='gallery', default='gallery/no-img.png')

    def __str__(self):
        return self.name


class User(models.Model):
    img = models.ImageField(upload_to='gallery', default='gallery/no-img.png')
    authentication = models.ForeignKey(uu, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return "User" + str(self.id)


class Review(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    media = models.ForeignKey(Media, on_delete=models.CASCADE)
    rate = models.PositiveIntegerField(default=0)
    review = models.CharField(max_length=1000)

    def __str__(self):
        return self.author + " - " + self.media
