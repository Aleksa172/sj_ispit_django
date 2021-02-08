from django.db import models
from games import models as gameModels
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class PlayerUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    achievements = models.ManyToManyField(gameModels.Achievement)
    games = models.ManyToManyField(gameModels.Game)

    def __str__(self):
        return self.user.username

    def hasGame(self, game_id):
        return self.games.filter(id=game_id).exists()

@receiver(post_save, sender=User)
def create_user_player_user(sender, instance, created, **kwargs):
    if created:
        PlayerUser.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_player_user(sender, instance, **kwargs):
    instance.playeruser.save()