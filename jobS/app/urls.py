from django.urls import path
from .import views
urlpatterns = [
    path('login/',views.ulogin,name='login'),
    path('register/',views.register,name='register'),
    path('',views.home,name='home'),
    path('jview/<int:pk>',views.jview,name='jview'),
    path('upload_resume/', views.upload_resume, name='upload_resume'),
    path('apply/<int:pk>', views.apply, name='apply'),
    path('cview/', views.cview, name='cview'),
    path('cjview/<int:pk>', views.cjview, name='cjview'),
    path('logout/', views.uLogout, name='logout'),
    path('create_job/', views.create_job, name='create_job'),
    path('search/', views.search, name='search'),
]