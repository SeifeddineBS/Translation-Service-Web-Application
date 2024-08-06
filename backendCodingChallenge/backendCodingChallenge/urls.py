from django.contrib import admin
from django.urls import path
from backendCodingChallenge import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('translations/',views.translation_list),
    path("translations/<int:id>", views.translation_details),
    path('signup', views.signup),
    path('login', views.login),
    path('test_token', views.test_token),
    path('logout', views.logout),


]
