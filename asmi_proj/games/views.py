from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Game, News, Achievement
from django.contrib.auth.models import User
from .forms import RegisterForm
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.conf.urls import url





from django.contrib.auth.decorators import login_required



def index(request):
    games_list = Game.objects.all().order_by('name')
    user_games_list = None
    if request.user.is_authenticated:
        user_games_list = request.user.playeruser.games.all()

    
    return render(request, 'game_index.html', {'games_list': games_list, 'user_games_list': user_games_list})

def games_details(request, game_id):
    # Ako igre nema, baci 404
    try:
        game = Game.objects.get(id=game_id)
    except Game.DoesNotExist:
        return render(request, '404.html')
    
    # Jednostavnija varijanta od games_indexa, jer je uvek jedna igra u pitanju
    user_has_game = False
    if request.user.is_authenticated:
        user_has_game = request.user.playeruser.games.filter(id=game_id).exists()

    try:
        news_list = News.objects.filter(game_id=game_id)
        if len(news_list) == 0:
            news_list = None
    except News.DoesNotExist:
        news_list = None

    return render(request, 'game_details.html', {'game': game, 'news_list': news_list, 'user_has_game': user_has_game})

def news_details(request, broj):
    try:
        news = News.objects.get(id=broj)
    except News.DoesNotExist:
        return render(request, '404.html')

    return render(request, 'news_details.html', {'news': news})

# APIji u kojima korisnik upravlja sam sobom
@login_required
def my_achievements(request, game_id):
    # Validacija 
    try:
        game = Game.objects.get(id=game_id)
        achievement_list = Achievement.objects.filter(game_id=game_id)
    except Game.DoesNotExist:
        return render(request, '404.html')
    
    # Validacija - Player has game?
    player_has_game = request.user.playeruser.games.filter(id=game_id).count()>0
    if not player_has_game:
        return redirect(reverse('root_index'))

    

    # Slanje forme
    if request.method == "POST":
        achievement_ids = request.POST.getlist("choice")
        
        # Validacija greske ukoliko je igra u medjuvremenu izbrisana
        if player_has_game == False:
            error_message = 'You appear not to have this game anymore. (Did you remove it on another tab meanwhile?). Please go back and add it first.'
            return render(request, 'players/player_myachievements.html', {'game': game, 'achievement_list': achievement_list, 'error_message': error_message})        
        
        # Da li ovi achievementi uopste pripadaju ovoj igri? Za slucaj da se neko glupira hakovanjem
        achievement_filter = Achievement.objects.filter(game_id=game_id, id__in=achievement_ids).count() == len(achievement_ids)
        if achievement_filter == False:
            error_message = 'Something went wrong. Please try again.'
            return render(request, 'players/player_myachievements.html', {'game': game, 'achievement_list': achievement_list, 'error_message': error_message})        

        selected_achievements = Achievement.objects.filter(id__in=achievement_ids)
        
        # Uklanjamo sve achievemente za igru
        # Mora da postoji bolji nacin da se ovo napise
        existing_achievements = request.user.playeruser.achievements.filter(game_id=game_id)
        if len(existing_achievements)>0:
            request.user.playeruser.achievements.remove(*existing_achievements)
        # Da bismo postavili novo stanje checkboxova
        request.user.playeruser.achievements.add(*selected_achievements)
        request.user.playeruser.save()
        messages.add_message(request, messages.INFO, 'Achievements saved!')
    
    # U suprotnom je normalni GET za moje achievemente
    # ili smo upravo zavrsili update
    user_achievement_list =  request.user.playeruser.achievements.filter(game_id=game_id)
    return render(request, 'players/player_myachievements.html', {'game': game, 'achievement_list': achievement_list, 'user_achievement_list': user_achievement_list})
    

"""
def edit_games(request, id):
    if request.method == "POST":
        form = GameForm(request.POST)

        if form.is_valid():
            g = Game.objects.get(id=id)
            g.name = form.cleaned_data['name']
            g.save()
            return redirect('games')
        else:
            return render(request, 'edit_games.html', {'form': form, 'id': id})
    else:
        g = Game.objects.get(id=id)
        form = GameForm(instance=g)
"""

@login_required
def my_add_game(request, game_id):
    try:
        game = Game.objects.get(id=game_id)
    except Game.DoesNotExist:
        return render(request, '404.html')    

    if request.user.playeruser.hasGame(game_id):
        messages.add_message(request, messages.INFO, 'You have already added this game')
        return HttpResponseRedirect(reverse('games_details', kwargs={'game_id':game_id}))
        

    if request.user.is_authenticated:
        request.user.playeruser.games.add(game)
        request.user.playeruser.save()

    # Vracamo ga na istu stranu
    return HttpResponseRedirect(reverse('games_details', kwargs={'game_id':game_id}))

@login_required
def my_remove_game(request, game_id):
    try:
        game = Game.objects.get(id=game_id)
    except Game.DoesNotExist:
        return render(request, '404.html')    

    if not request.user.playeruser.hasGame(game_id):
        messages.add_message(request, messages.INFO, 'But... you didn\'t even have the game.')
        return HttpResponseRedirect(reverse('games_details', kwargs={'game_id':game_id}))
        

    if request.user.is_authenticated:
        request.user.playeruser.games.remove(game)
        # Brisemo i achievemente
        existing_achievements = request.user.playeruser.achievements.filter(game_id=game_id)
        if len(existing_achievements)>0:
            request.user.playeruser.achievements.remove(*existing_achievements)
        request.user.playeruser.save()

    # Vracamo ga na istu stranu
    return HttpResponseRedirect(reverse('games_details', kwargs={'game_id':game_id}))




# Registracija -
def custom_register(request):

    if request.method == "POST":
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            data = form.cleaned_data
            enc_pass = make_password(data["password"])
            username = data["username"]
            newu = User.objects.create(username=username, password=enc_pass)
            newu.save()
            success_message = "Your have successfully registered! Please feel free to login with your new account." 
            return render(request, 'registration/register.html', {'form': form, 'success_message': success_message})

        # Nesto nije uspelo
        return render(request, 'registration/register.html', {'form': form})

    # Osnovna forma, dosao sa GET
    form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form}) 

def player_profile_games(request, usr_id):
    try:
        profile = User.objects.get(id=usr_id)
    except User.DoesNotExist:
        return render(request, '404.html')    

    user_games_list = None
    if request.user.is_authenticated:
        # Ako pokusam da gledam svoj profil kao tuđi, a moj je:
        # redirectuj me na index kao da sam ulogovan
        if request.user.id == profile.id:
            return redirect(reverse('root_index'))

        # Moje igre - ako sam ulogovan
        user_games_list = request.user.playeruser.games.all()

    # Igre drugog igraca
    profile_game_list = profile.playeruser.games.all()
    if len(profile_game_list)==0:
        profile_game_list = None
    
    
    
    return render(request, 'players/player_profile.html', {'profile': profile, 'games_list': profile_game_list, 'user_games_list': user_games_list})


def player_profile_achievements(request, usr_id, game_id):
    # Validacija 
    # Da li igra postoji?
    try:
        game = Game.objects.get(id=game_id)
        achievement_list = Achievement.objects.filter(game_id=game_id)
    except Game.DoesNotExist:
        return render(request, '404.html')

    # Da li trazeni profil postoji?
    try:
        profile = User.objects.get(id=usr_id)
    except User.DoesNotExist:
        return render(request, '404.html')    
    
    # Validacija - Profil has game?
    player_has_game = profile.playeruser.games.filter(id=game_id).count()>0
    if not player_has_game:
        return render(request, '404.html')

    user_achievement_list = None
    # Ako sam ulogovan, mogu poredim achievemente!
    if request.user.is_authenticated:
        user_achievement_list =  request.user.playeruser.achievements.filter(game_id=game_id)
    profile_achievement_list = profile.playeruser.achievements.filter(game_id=game_id)

    return render(request, 'players/player_achievements.html', {'game': game, 
        'profile': profile,
        'achievement_list': achievement_list, 
        'profile_achievements_list': profile_achievement_list, 
        'user_achievement_list': user_achievement_list})


def list_profiles(request):
    search = None

    if request.method == "GET" and request.GET.get('search',None) is not None:
        search = request.GET.get('search')

    if request.user.is_authenticated:
        # Vrati listu bez mene
        if search is None:
            profiles = User.objects.exclude(id=request.user.id)
        else:
            profiles = User.objects.exclude(id=request.user.id).filter(username__contains=search)
    else:
        if search is None:
            profiles = User.objects.all()
        else:
            profiles = User.objects.filter(username__contains=search)

    return render(request, 'players/player_list.html', {'profile_list': profiles, 'search': search})

def parametri(request):
    for k,v in request.GET.items():
        print(k,v)

def hello_django(request):
    return render(request, 'hello.html')