from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name="games_index"),
    path('hello_html', views.hello_django, name="games_html"),
    path('profiles', views.list_profiles, name="list_profiles"),
    path('<game_id>', views.games_details, name="games_details"),
    path('news/<broj>', views.news_details, name="news_details"),
    path('my/game/<game_id>/achievements', views.my_achievements, name="myachievements"),
    path('my/game/<game_id>/add', views.my_add_game, name="mygame_add"),
    path('my/game/<game_id>/remove', views.my_remove_game, name="mygame_remove"),
    path('player/<usr_id>/games', views.player_profile_games, name="player_games"),
    path('player/<int:usr_id>/game/<int:game_id>', views.player_profile_achievements, name="player_achievements"),
    
]


