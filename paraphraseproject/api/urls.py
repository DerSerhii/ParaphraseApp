from django.urls import path

from .API.resources import ParaphraseAPIView


urlpatterns = [
    path('paraphrase/', ParaphraseAPIView.as_view()),
]
