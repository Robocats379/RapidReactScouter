from django.shortcuts import render
from teams.models import Team
from matches.models import ScoutedMatch

# Create your views here.
def team_list(request):
    teams = Team.objects.all()
    return render(request, "team-list.html", context={'teams': teams})

def team_detail(request, pk):
    team = Team.objects.get(team_number=pk)
    matches = ScoutedMatch.objects.filter(team=team).order_by('match__number')
    notes = matches.exclude(notes="")
    context = {
        'team': team,
        'matches': matches,
        'notes': notes
    }
    return render(request, "team-detail.html", context=context)