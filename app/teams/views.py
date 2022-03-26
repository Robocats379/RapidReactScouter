from django.shortcuts import render
from teams.models import Team
from matches.models import ScoutedMatch

# Create your views here.
def team_list(request):
    teams = Team.objects.all()
    return render(request, "team-list.html", context={'teams': teams, 'page_name': 'All Teams'})

def pick_list(request):
    teams = Team.objects.filter(team_number__in=[
        340,
        3015,
        4028,
        5740,
        3003,
        1507,
        120,
        3504,
        3173,
        191,
        3193,
        7165,
        378,
        3324,
        1317,
        1559,
        1405,
        6181,
        1518,
        695,
        2603,
        4121,
        48,
        3173,
        4930,
        4145,
        5740,
        578,
        2172
    ])
    context = {
        'teams':teams,
        'page_name': "Pick List"
    }
    return render(request, "team-list.html", context=context)


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