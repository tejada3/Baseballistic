from django.db import models


class Teams(models.Model):
    team_id = models.CharField(max_length=50, db_index=True)
    team_name = models.TextField(max_length=50, db_index=True)

    class Meta:
        ordering = ['team_name']

    def __str__(self):
        return self.team_name


class TeamSelector(models.Model):
    option = models.ForeignKey(Teams, on_delete=models.CASCADE, null=True)