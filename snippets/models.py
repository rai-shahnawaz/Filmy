from django.db import models
import datetime
from django.contrib.auth.models import User

# Create your models here.
GENDER_CHOICES = [
       ('M', 'Male'),
       ('F', 'Female'),
       ('O', 'Other'),
   ]


class Badge(models.Model):
    name = models.IntegerField(null=True)
    removed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    
class Genre(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    available = models.BooleanField()
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, blank=True, null=True)
    removed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    
class SubGenre(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    available = models.BooleanField()
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, blank=True, null=True)
    removed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    
class Award(models.Model):
    country = models.CharField(max_length=100, blank=True)
    name = models.CharField(max_length=100)
    year = models.DateField(blank=True, null=True)
    removed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)   
    

class Film(models.Model):
    title = models.CharField(max_length=100)
    released_on = models.DateField()
    plot = models.TextField(blank=True)
    animated = models.BooleanField(default=False)
    rating = models.IntegerField(null=True)
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, blank=True, null=True)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, blank=True, null=True)
    subgenre = models.ForeignKey(SubGenre, on_delete=models.CASCADE, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True)    
    language = models.CharField(max_length=100, blank=True)
    awards = models.ForeignKey(Award, on_delete=models.CASCADE, blank=True, null=True)
    available = models.BooleanField(default=False)
    removed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    
class Series(models.Model):
    title = models.CharField(max_length=100)
    aired_on = models.DateField()
    unaired_on = models.DateField(blank=True, null=True)
    plot = models.TextField(blank=True)
    animated = models.BooleanField(default=False)
    rating = models.IntegerField(null=True)
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, blank=True, null=True)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, blank=True, null=True)
    subgenre = models.ForeignKey(SubGenre, on_delete=models.CASCADE, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True)    
    language = models.CharField(max_length=100, blank=True)
    awards = models.ForeignKey(Award, on_delete=models.CASCADE, blank=True, null=True)
    available = models.BooleanField(default=False)
    removed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    
class Season(models.Model):
    series = models.ForeignKey(Series, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    aired_on = models.DateField()
    unaired_on = models.DateField(blank=True, null=True)
    plot = models.TextField(blank=True)
    animated = models.BooleanField(default=False)
    rating = models.IntegerField(null=True)
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True)    
    language = models.CharField(max_length=100, blank=True)
    awards = models.ForeignKey(Award, on_delete=models.CASCADE, blank=True, null=True)
    available = models.BooleanField(default=False)
    removed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    
class Episode(models.Model):
    series = models.ForeignKey(Series, on_delete=models.CASCADE)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    aired_on = models.DateField()
    unaired_on = models.DateField(blank=True, null=True)
    plot = models.TextField(blank=True)
    animated = models.BooleanField(default=False)
    rating = models.IntegerField(null=True)
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True)    
    language = models.CharField(max_length=100, blank=True)
    awards = models.ForeignKey(Award, on_delete=models.CASCADE, blank=True, null=True)
    available = models.BooleanField(default=False)
    removed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    

class Director(models.Model):
    film = models.ManyToManyField(Film)
    series = models.ManyToManyField(Series)
    name = models.CharField(max_length=100)
    dob = models.DateField(blank=True, null=True)
    dod = models.DateField(default=None, blank=True, null=True)
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, blank=True, null=True)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, blank=True, null=True)
    subgenre = models.ForeignKey(SubGenre, on_delete=models.CASCADE, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True)    
    state = models.CharField(max_length=100, blank=True)  
    city = models.CharField(max_length=100, blank=True)  
    awards = models.ForeignKey(Award, on_delete=models.CASCADE, blank=True, null=True)
    removed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def full_name(self):
        return '%s %s' % (self.first_name, self.last_name)
    
    
class Actor(models.Model):
    film = models.ManyToManyField(Film)
    series = models.ManyToManyField(Series)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=100, choices=GENDER_CHOICES)
    dob = models.DateField(blank=True, null=True)
    dod = models.DateField(default=None, blank=True, null=True)
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, blank=True, null=True)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, blank=True, null=True)
    subgenre = models.ForeignKey(SubGenre, on_delete=models.CASCADE, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True)    
    state = models.CharField(max_length=100, blank=True)  
    city = models.CharField(max_length=100, blank=True)
    awards = models.ForeignKey(Award, on_delete=models.CASCADE, blank=True, null=True)
    removed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    gender = models.CharField(max_length=100, choices=GENDER_CHOICES, blank=True)
    dob = models.DateField(blank=True, null=True)
    email = models.EmailField(max_length=256)
    password = models.CharField(max_length=100)
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True)    
    state = models.CharField(max_length=100, blank=True)  
    city = models.CharField(max_length=100, blank=True)
    removed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.first_name
    
    def full_name(self):
        return '%s %s' % (self.first_name, self.last_name)
    
    def calculate_age(self):
        today = datetime.date.today()
        try: 
            birthday = self.dob.replace(year=today.year)
        # raised when birth date is February 29 and the current year is not a leap year
        except ValueError:
            birthday = self.dob.replace(year=today.year, day=self.dob.day-1)

        if birthday > today:
            return today.year - self.dob.year - 1
        else:
            return today.year - self.dob.year
    
    
class Wishlist(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    film = models.ForeignKey(Film, on_delete=models.CASCADE, blank=True, null=True)
    series = models.ForeignKey(Series, on_delete=models.CASCADE, blank=True, null=True)
    removed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user.first_name + "'s wishlist"
    
    
class Watchedlist(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    film = models.ForeignKey(Film, on_delete=models.CASCADE, blank=True, null=True)
    series = models.ForeignKey(Series, on_delete=models.CASCADE, blank=True, null=True)
    removed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user.first_name + "'s watchedlist"
    
    
class CustomerRating(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    film = models.ForeignKey(Film, on_delete=models.CASCADE, blank=True, null=True)
    series = models.ForeignKey(Series, on_delete=models.CASCADE, blank=True, null=True)
    rating = models.IntegerField(null=True)
    removed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user.first_name + "'s ratings"
    
    
class Favourite(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    film = models.ForeignKey(Film, on_delete=models.CASCADE, blank=True, null=True)
    series = models.ForeignKey(Series, on_delete=models.CASCADE, blank=True, null=True)
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE, blank=True, null=True)
    director = models.ForeignKey(Director, on_delete=models.CASCADE, blank=True, null=True)
    removed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user.first_name + "'s favourite"
    