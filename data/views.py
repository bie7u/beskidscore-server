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
        serializer = EventSerializer({'events': events})
        return Response(serializer.data)


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
    filterset_fields = ['league', 'season']


class SeasonViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = SeasonM.objects.all()
    serializer_class = SeasonSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['league']
