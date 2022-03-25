from django.shortcuts import render
from teams.models import Team

# Create your views here.
def team_list(request):
    teams = Team.objects.all()
    return render(request, "team-list.html", context={'teams': teams})