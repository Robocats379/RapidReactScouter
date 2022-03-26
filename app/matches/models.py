from django.db import models
import uuid

# Create your models here.
class Match(models.Model):
    MATCH_TYPE_CHOICES = [
        ("PRACTICE", "Practice"),
        ("QUALIFICATION", "Qualification"),
        ("PLAYOFF", "Playoff")
    ]

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    type = models.CharField(max_length=255, choices=MATCH_TYPE_CHOICES)
    number = models.IntegerField()

    class Meta:
        verbose_name_plural = "Matches"

    def __str__(self):
        return f"{self.get_type_display()} - {self.number}"


class ScoutedMatch(models.Model):
    ALLIANCE_CHOICES = [
        ("RED", "Red"),
        ("BLUE", "Blue")
    ]

    CARGO_START_CHOICES = [
        (0, 0),
        (1, 1)
    ]

    CARGO_PICKUP_LOCATION_CHOICES = [
        ("FLOOR", "Floor"),
        ("HUMAN PLAYER", "Human Player"),
        ("N/A", "N/A")
    ]

    CARGO_SCORED_LOCATIONS = [
        ("UPPER GOAL", "Upper Goal"),
        ("LOWER GOAL", "Lower Goal"),
        ("BOTH GOALS", "Both Goals"),
        ("N/A", "N/A")
    ]

    CLIMB_STATUS_CHOICES = [
        ("YES", "Yes"),
        ("NO", "No"),
        ("FAILED", "Failed")
    ]

    uuid = models.UUIDField(editable=False, unique=True, default=uuid.uuid4)
    alliance = models.CharField(max_length=255, choices=ALLIANCE_CHOICES)
    team = models.ForeignKey('teams.Team', on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    scouted_by = models.CharField(max_length=255)
    did_participate = models.BooleanField()

    #Auto
    auto_cargo_start_count = models.IntegerField(choices=CARGO_START_CHOICES)
    auto_does_cross_scoring_line = models.BooleanField()
    auto_does_shoot = models.BooleanField()
    auto_does_score_cargo = models.BooleanField()
    auto_cargo_scored_high = models.IntegerField(default=0)
    auto_cargo_scored_low = models.IntegerField(default=0)

    #Teleop
    teleop_where_get_cargo = models.CharField(max_length=255, choices=CARGO_PICKUP_LOCATION_CHOICES)
    teleop_effective_floor_cargo = models.BooleanField()
    teleop_does_score_cargo = models.BooleanField()
    teleop_cargo_score_location = models.CharField(max_length=255, choices=CARGO_SCORED_LOCATIONS)
    teleop_attempted_shots = models.IntegerField(default=0)
    teleop_missed_shots = models.IntegerField(default=0)
    teleop_can_shoot_launch_pad = models.BooleanField()
    teleop_can_shoot_tarmac = models.BooleanField()
    teleop_can_shoot_carpet = models.BooleanField()
    teleop_can_shoot_against_hub = models.BooleanField()
    teleop_does_play_defense = models.BooleanField()
    teleop_defense_effective = models.BooleanField()

    #End Game
    end_does_climb = models.CharField(max_length=255, choices=CLIMB_STATUS_CHOICES)
    end_climb_first_rung = models.BooleanField()
    end_climb_second_rung = models.BooleanField()
    end_climb_traversal = models.BooleanField()
    end_points_scored = models.IntegerField()

    notes = models.TextField(blank=True, default="")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        team = self.team
        matches = ScoutedMatch.objects.filter(team=self.team)
        team.total_match_count = matches.count()

        team.participation_count = 0
        team.one_ball_start_count = 0
        team.zero_ball_start_count = 0
        team.teleop_attempted_shot_count = 0
        team.teleop_missed_shot_count = 0
        team.climb_count = 0
        team.traversal_count = 0
        team.auto_low_cargo_count = 0
        team.auto_high_cargo_count = 0


        for match in matches:
            if match.did_participate:
                team.participation_count += 1
            if match.auto_cargo_start_count == 1:
                team.one_ball_start_count += 1
            if match.auto_cargo_start_count == 0:
                team.zero_ball_start_count += 1
            team.teleop_attempted_shot_count += match.teleop_attempted_shots
            team.teleop_missed_shot_count += match.teleop_missed_shots
            if match.end_does_climb == "YES":
                team.climb_count += 1
            if match.end_climb_traversal:
                team.traversal_count += 1
            team.auto_low_cargo_count += match.auto_cargo_scored_low
            team.auto_high_cargo_count += match.auto_cargo_scored_high
        team.save()



