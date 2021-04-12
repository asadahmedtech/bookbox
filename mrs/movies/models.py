from django.db import models

# Create your models here.

# City Model for defining the cities
class City(models.Model):
    city_choice=(
        ('BANGALORE','Bangalore'),
        ('CHENNAI','Chennai'),
        ('DELHI','Delhi'),
        ('HYDERABAD','Hyderabad'),
        ('KOLKATA','Kolkata'),
        ('MUMBAI','Mumbai'),
    )

    city = models.CharField(max_length=30, null=False, choices=city_choice)
    state = models.CharField(max_length=30, null=True)
    zipcode = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return '{}-{}-{}'.format(self.state, self.city, self.zipcode)

# Theater Model for defining the theaters in the cities
class Theater(models.Model):
    name = models.CharField(max_length=100, null=False, default="Default Cinema")
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)

    def __str__(self):
        return '{}-{}-{}'.format(self.name, self.address, self.city)

# TheaterSeat Model for defining the seats in the theaters
class TheaterSeat(models.Model):
    seat_choice = (
        ('PREMIUM','Premium'),
        ('NORMAL','Normal'),
        ('RECLINER','Recliner'),
        ('FRONT','Front'),
    )
    seatNumber = models.CharField(max_length=5, null=False)
    seatType = models.CharField(max_length=20, null=False, choices=seat_choice)
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE)

    def __str__(self):
        return '{}-{}-{}'.format(self.seatNumber, self.seatType, self.theater)

# Movie model for defining the movies currently being shown
class Movie(models.Model):
    lang_choice = (
        ('ENGLISH', 'English'),
        ('BENGALI', 'Bengali'),
        ('HINDI', 'Hindi'),
        ('TAMIL', 'Tamil'),
        ('TELUGU', 'Telugu'),
        ('KANNADA', 'Kannada')
    )
    rating_choice = (
        ('U', 'U'),
        ('UA', 'U/A'),
        ('A', 'A'),
        ('R', 'R'),
    )

    name = models.CharField(max_length=50, null=False)
    cast = models.CharField(max_length=100, null=True, blank=True)
    director = models.CharField(max_length=50, null=True, blank=True)
    language = models.CharField(max_length=10, choices=lang_choice)
    run_length = models.IntegerField(null=True, blank=True)
    certificate = models.CharField(max_length=2, choices=rating_choice)
    image = models.ImageField(null=True, blank=True, upload_to='media')

    def __str__(self):
        return self.name

# Show model for defining the showtimes of movies in each threater. Linked to Theater and Movie using FK.
class Show(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE)
    show_time = models.DateTimeField()

    def __str__(self):
        return '{}-{}-{}'.format(self.movie, self.theater,self.show_time)

