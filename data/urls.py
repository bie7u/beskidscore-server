from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    HealthCheckView, LeagueViewSet, TeamViewSet, MatchViewSet,
    StandingViewSet, RoundViewSet, SeasonViewSet, MessengerWebhookView, update_match
)


router = DefaultRouter()
router.register(r'leagues', LeagueViewSet)
router.register(r'teams', TeamViewSet)
router.register(r'matches', MatchViewSet)
router.register(r'standings', StandingViewSet)
router.register(r'rounds', RoundViewSet)
router.register(r'seasons', SeasonViewSet)

urlpatterns = [
    path('health', HealthCheckView.as_view(), name='health_check'),
    path('webhook/', MessengerWebhookView.as_view(), name='messenger-webhook'),
    path('', include(router.urls)),
    path('update_match/<int:match_id>/', update_match, name='update_match_detail'),
]