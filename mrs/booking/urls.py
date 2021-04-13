from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from booking import views

urlpatterns = [
    path('book/', views.BookingList.as_view()),
    path('seat/', views.ShowSeatList.as_view()),
    path('payment/', views.PaymentList.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)
