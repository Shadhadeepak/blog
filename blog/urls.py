from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('post/<str:slug>/', views.detail, name='detail'),
    path('old-index/', views.old_url_redirect, name='old index'),
    path('new_url/', views.new_url_view, name='new_page_url'),
    path('contact/', views.contact_view, name='contact'),  
    path('about/', views.about_view, name='about'),        
    path('register/', views.register, name='register'),        
    path('login/', views.login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout, name='logout'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password/<uidb64>/<token>/', views.reset_password, name='reset_password'),
    path('new_post/', views.new_post, name='new_post'),
    path('edit_post/<int:post_id>', views.edit_post, name='edit_post'),
    path('delete_post/<int:post_id>', views.delete_post, name='delete_post'),
    
]