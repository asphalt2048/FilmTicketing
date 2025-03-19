from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('', views.login_view),
    path('seats_detail/', views.seats_detail),
    path('timeslot_info/', views.timeslot_info),
    path('actor/', views.actor),
    path('film_list/', views.film_list),
    path('search_film/', views.search_film),
    path('timeslot_list/', views.timeslot_list),
    path('avai_seat/', views.avai_seat),
    path('total_seat/', views.total_seat),
    path('user/register/', views.register),
    path('user/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/id/', views.test, name='user_detail'),
    path('user/timeslot/seats_number/', views.user_order_in_timeslot),
    path('order_seats/', views.order_seats),
    path('user/user_orders/', views.user_orders),
    path('user/cancel_order/', views.cancel_order),
    path('user/pay_booked/', views.pay_booked),
    path('submit_rating/', views.submit_rating),
    path('film_avg_rating/', views.film_avg_rating),
]


