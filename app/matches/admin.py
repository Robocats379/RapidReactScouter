from django.contrib import admin
from .models import Match, ScoutedMatch

# Register your models here.
admin.site.register(Match)
admin.site.register(ScoutedMatch)