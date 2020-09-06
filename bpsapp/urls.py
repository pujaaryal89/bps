from django.urls import path
from .views import Visitorhome_view,registration_view
from .views import login_view,logout_view
from .views import location_view,locationreview_view,locationdetail_view,locationreviewdelete_view

app_name = 'bpsapp'
urlpatterns = [
  path('',Visitorhome_view,name='visitorhome'),
  path("register/",registration_view,name='register'),
  path("login/",login_view,name='login'),
  path("logout/",logout_view,name='logout'),
  path("location/",location_view,name='location'),
  path("locationdetail/<int:detail_pk>/",locationdetail_view,name='locationdetail'),
  path("locationreview/<int:location_pk>/",locationreview_view,name='locationreview'),
  path("locationreviewdelete/<int:reviewdelete_pk>/",locationreviewdelete_view,name='locationreviewdelete'),






]