from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import LeagueM, SeasonM, TeamM, RoundM, MatchM, StandingM
from .serializers import (
    LeagueSerializer, SeasonSerializer, TeamSerializer, RoundSerializer,
    MatchSerializer, EventSerializer, StandingSerializer,
)
from rest_framework import mixins, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from data.filters import MatchFilter, LeagueFilter



class HealthCheckView(APIView):
    """Health check endpoint"""

    def get(self, request):
        return Response({
            'status': 'OK',
            'message': 'FlashScore Django API is running'
        })


class LeagueViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = LeagueM.objects.all()
    serializer_class = LeagueSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = LeagueFilter


class TeamViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = TeamM.objects.all()
    serializer_class = TeamSerializer


class MatchViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = MatchM.objects.all()
    serializer_class = MatchSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = MatchFilter

    @action(detail=True, methods=['get'])
    def events(self, request, pk=None):
        match = self.get_object()
        events = match.events.all()
        serializer = EventSerializer(events, many=True)
        return Response('siema')


class StandingViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = StandingM.objects.all()
    serializer_class = StandingSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['league', 'season']

    # @action(detail=False, methods=['post'])
    # def update_all(self, request):
    #     """Update all standings based on match results"""
    #     try:
    #         out = StringIO()
    #         call_command('update_standings', stdout=out)
    #         output = out.getvalue()
    #
    #         return Response({
    #             'status': 'success',
    #             'message': 'Standings updated successfully',
    #             'details': output
    #         })
    #     except Exception as e:
    #         return Response({
    #             'status': 'error',
    #             'message': f'Failed to update standings: {str(e)}'
    #         }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    #
    # @action(detail=True, methods=['post'])
    # def update_single(self, request, pk=None):
    #     """Update a specific standing based on match results"""
    #     try:
    #         standing = get_object_or_404(Standing, pk=pk)
    #         out = StringIO()
    #         call_command('update_standings',
    #                      league=standing.league.id,
    #                      season=standing.season.id,
    #                      stdout=out)
    #         output = out.getvalue()
    #
    #         return Response({
    #             'status': 'success',
    #             'message': f'Standing {standing} updated successfully',
    #             'details': output
    #         })
    #     except Exception as e:
    #         return Response({
    #             'status': 'error',
    #             'message': f'Failed to update standing: {str(e)}'
    #         }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RoundViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = RoundM.objects.all()
    serializer_class = RoundSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['league', 'season', 'season__year']


class SeasonViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = SeasonM.objects.all()
    serializer_class = SeasonSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['league']

from django.shortcuts import get_object_or_404, render


def update_match(request, match_id=None):
    match = get_object_or_404(MatchM, pk=match_id)
    if match.status == 'LIVE':
        if request.method == "POST":
            home_score = request.POST.get('home_score')
            away_score = request.POST.get('away_score')
            print(home_score, away_score)
            # Validate and update match
            match.home_score = home_score
            match.away_score = away_score
            match.save()
            # Redirect or show success
            return render(request, 'update_match.html', {'match': match, 'success': True})
        return render(request, 'update_match.html', {'match': match})
    return HttpResponse("Match is not live", status=403)

from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from .fb_client import send_message
from .match_client import get_active_matches, post_match_result
import os

FB_VERIFY_TOKEN = '123aaaaa'

class MessengerWebhookView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        # Webhook verification
        verify_token = request.GET.get("hub.verify_token")
        challenge = request.GET.get("hub.challenge")
        if verify_token == FB_VERIFY_TOKEN:
            return HttpResponse(challenge)
        return HttpResponse("Invalid verification token", status=403)

    def post(self, request):
        # return 
        data = request.data
        for entry in data.get("entry", []):
            for messaging in entry.get("messaging", []):
                sender_id = messaging["sender"]["id"]
                if "message" in messaging and "text" in messaging["message"]:
                    # User sent a normal message, show matches
                    live_matches = MatchM.objects.filter(status='LIVE')
                    matches = [{'id': match.id,
                                'match': f'{match.home_team.name} vs {match.away_team.name}'} for match in live_matches]
                    buttons = [
                                  {
            "type": "web_url",
            "url": f"https://ddd628b7480c.ngrok-free.app/api/update_match/{match['id']}/",
            "title": match['match'],
            "webview_height_ratio": "compact",
            # "messenger_extensions": 'true'
          } for match in matches
                    ]

                    # buttons = [
                    #     {
                    #         "type": "postback",
                    #         "title": match["name"],
                    #         "payload": f"MATCH_{match['id']}"
                    #     }
                    #     for match in matches
                    # ]
         
                    send_message(sender_id, buttons)
                elif "postback" in messaging:
                    payload = messaging["postback"]["payload"]
                    if payload.startswith("MATCH_"):
                        match_id = payload.split("_")[1]
                        # Send options for result
                        buttons = [
                            {"type": "postback", "title": "Win", "payload": f"RESULT_{match_id}_win"},
                            {"type": "postback", "title": "Lose", "payload": f"RESULT_{match_id}_lose"},
                            {"type": "postback", "title": "Draw", "payload": f"RESULT_{match_id}_draw"},
                        ]
                        send_message(sender_id, {
                            "text": "Select result:",
                            "buttons": buttons
                        })
                    elif payload.startswith("RESULT_"):
                        _, match_id, result = payload.split("_")
                        post_match_result(match_id, result)
                        send_message(sender_id, {"text": f"Result '{result}' submitted for match {match_id}!"})
        return Response({"status": "ok"})
    