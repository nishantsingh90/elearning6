from django.urls import path
from django.shortcuts import reverse


from . import views

app_name = 'product'

urlpatterns = [
    path('', views.index, name="index"),
    path('blog/', views.post_list, name='post-list'),
    # path('(?P<pk>[0-9]+)/$', views.post_detail, name='post-detail'),
    path('product/<slug>/', views.PostDetailView.as_view(), name='post-detail'),
    path('create/', views.PostCreateView.as_view(), name='post-create'),
    path('postcreatestaff/', views.PostCreateStaffView.as_view(), name='post-createstaff'),
    path('search/', views.search, name='search'),
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('(?P<username>[a-zA-Z0-9]+)$', views.get_user_profile,name="profile"),
    path('following/(?P<user>[a-zA-Z0-9]+)$', views.follow_user,name="follow"),
    path('ghar(?P<user>[a-zA-Z0-9]+)$', views.unfollow_user,name="unfollow"),
    path('updateprofile/', views.update_profile, name="update_profile"),
    
    
    # path('post/<id>/',views.post_detail, name='post-detail'),

]