from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.urls import reverse


# Create your models here.
class Developer(models.Model):
    name=models.CharField(max_length=100);

    def __str__(self):
        return self.name

class Game(models.Model):
    name=models.CharField(max_length=100);
    description=models.TextField();
    steam_link=models.CharField(max_length=200);
    release_year=models.IntegerField();
    developer = models.ForeignKey(Developer, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

    def get_game_url(self):
        return reverse('games_details', args=[str(self.id)])

class Achievement(models.Model):
    name=models.CharField(max_length=60);
    description=models.TextField();
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    gamer_points=models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)]);

    def __str__(self):
        return self.name

class News(models.Model):
    class Meta:
        verbose_name_plural = "News"

    title=models.CharField(max_length=100);
    content=models.TextField();
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    

    def __str__(self):
        return self.title + " - " + self.created.strftime("%d.%m.%Y - %H:%M:%S")

    def get_absolute_url(self):
        return reverse('news_details', args=[str(self.id)])

    def get_game_url(self):
        return self.game.get_game_url()

    def get_published_date(self):
        return self.created.strftime("%d.%m.%Y - %H:%M:%S")