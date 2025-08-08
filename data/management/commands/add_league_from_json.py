# data/management/commands/add_league_from_json.py
from django.db import transaction
from django.core.management.base import BaseCommand
from data.models import LeagueM, SeasonM, TeamM, RoundM, MatchM
import json
import os


class Command(BaseCommand):
    help = 'Adds a league from a JSON file'

    def handle(self, *args, **options):
        current_dir = os.path.dirname(__file__)
        json_path = os.path.join(current_dir, 'output.json')

        # Open and load JSON file
        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        with transaction.atomic():
            league = LeagueM.objects.create(name='B Klasa Bielsko Biala')
            season = SeasonM.objects.create(year='2025', name='2024/2025', season_years='2024/2025',  league=league)

            for round_info in data:
                round_name = round_info["round"]
                print(round_name)
                round_number = int(round_name.split()[1])
                round_obj = RoundM.objects.create(round_number=round_number, name=round_name, league=league, season=season)
                print(round_number)
                for match in round_info["matches"]:
                    home_team_obj = TeamM.objects.get_or_create(name=match["home_team"])[0]
                    away_team_obj = TeamM.objects.get_or_create(name=match["away_team"])[0]
                    match_obj = MatchM.objects.create(round=round_obj, league=league, season=season,
                                                      home_team=home_team_obj, away_team=away_team_obj,
                                                      home_score=match["home_score"], away_score=match["away_score"],
                                                      status='FINISHED',)
                # a = {
                #     "round": round_name,
                #     "date_time": match["date_time"],
                #     "home_team": match["home_team"],
                #     "home_score": match["home_score"],
                #     "away_team": match["away_team"],
                #     "away_score": match["away_score"]
                # }
                # print(a)
