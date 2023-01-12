from django.urls import path

from .views import SchuelerViewSet

urlpatterns = [
    path('schueler', SchuelerViewSet.as_view({
        'get':'check_user_distribution'
    }))
]