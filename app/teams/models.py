from django.db import models
import uuid
import tbaapiv3client
from tbaapiv3client.rest import ApiException

configuration = tbaapiv3client.Configuration(
    host = "https://www.thebluealliance.com/api/v3",
    api_key = {
        'X-TBA-Auth-Key': 'UlN7JY7VgFudrHWCiSvWimYoT8I6rD6n5aEqJzTh6sVP01Dh5EvFR4hR87EAlT2c'
    }
)

class Team(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    team_number = models.IntegerField()
    nickname = models.CharField(default="", max_length=256, blank=True)
    city = models.CharField(default="", max_length=255, blank=True)
    rookie_year = models.IntegerField(default=None, null=True, blank=True)
    state = models.CharField(max_length=255, default="", blank=True)

    total_match_count = models.IntegerField(default=0, blank=True)
    participation_count = models.IntegerField(default=0, blank=True)

    one_ball_start_count = models.IntegerField(default=0, blank=True)
    zero_ball_start_count = models.IntegerField(default=0, blank=True)
    crossed_scoring_line_count = models.IntegerField(default=0, blank=True)
    auto_shoot_count = models.IntegerField(default=0, blank=True)
    auto_score_count = models.IntegerField(default=0, blank=True)
    auto_high_cargo_count = models.IntegerField(default=0, blank=True)
    auto_low_cargo_count = models.IntegerField(default=0, blank=True)

    teleop_pickup_human_player_count = models.IntegerField(default=0, blank=True)
    teleop_pickup_floor_count = models.IntegerField(default=0, blank=True)
    teleop_effective_floor_pickup_count = models.IntegerField(default=0, blank=True)
    teleop_scores_cargo_count = models.IntegerField(default=0, blank=True)
    teleop_attempted_shot_count = models.IntegerField(default=0, blank=True)
    teleop_missed_shot_count = models.IntegerField(default=0, blank=True)
    teleop_defense_count = models.IntegerField(default=0, blank=True)
    teleop_defense_effective_count = models.IntegerField(default=0, blank=True)
    teleop_against_hub_count = models.IntegerField(default=0, blank=True)
    teleop_launch_pad_count = models.IntegerField(default=0, blank=True)
    teleop_tarmac_count = models.IntegerField(default=0, blank=True)
    teleop_carpet_count = models.IntegerField(default=0, blank=True)


    failed_climb_count = models.IntegerField(default=0, blank=True)
    end_points_scored_count = models.IntegerField(default=0, blank=True)
    first_rung_count = models.IntegerField(default=0, blank=True)
    second_rung_count = models.IntegerField(default=0, blank=True)
    traversal_count = models.IntegerField(default=0, blank=True)







    class Meta:
        ordering = ('team_number',)


    def save(self, *args, **kwargs):
        with tbaapiv3client.ApiClient(configuration) as api_client:
            # Create an instance of the API class
            api_instance = tbaapiv3client.TeamApi(api_client)
            try:
                api_response = api_instance.get_team(team_key=f"frc{self.team_number}")
                self.nickname = api_response.nickname
                self.city = api_response.city
                self.rookie_year = api_response.rookie_year
                self.state = api_response.state_prov
            except ApiException as e:
                print("Exception when calling TBAApi->get_status: %s\n" % e)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Team {self.team_number}: {self.nickname}"

    @property
    def accuracy(self):
        if (self.teleop_attempted_shot_count + self.teleop_missed_shot_count) == 0:
            return f"N/A"
        return f"{round(self.teleop_attempted_shot_count / (self.teleop_attempted_shot_count + self.teleop_missed_shot_count) * 100,2)}%"