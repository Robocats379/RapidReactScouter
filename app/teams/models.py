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