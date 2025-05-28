# main_app/urls.py
from django.urls import path
from . import views

app_name = 'main_app'

urlpatterns = [
    # ... (All URLs from Sprint 6 up to my_submissions) ...
    path('', views.index, name='index'),
    path('errors/', views.error_list, name='error_list'),
    path('error/<slug:error_slug>/', views.error_detail, name='error_detail'),
    path('category/<slug:category_slug>/', views.errors_by_category, name='errors_by_category'),
    path('categories/', views.category_list, name='category_list'),
    path('search/', views.search_results, name='search_results'),
    path('bookmarks/', views.my_bookmarks, name='my_bookmarks'),
    path('bookmark/add/<slug:error_slug>/', views.add_bookmark, name='add_bookmark'),
    path('bookmark/remove/<slug:error_slug>/', views.remove_bookmark, name='remove_bookmark'),
    path('submit-error/', views.submit_error, name='submit_error'),
    path('my-submissions/', views.my_submissions, name='my_submissions'),

    # New URL for Sprint 7: User Profile
    path('profile/<str:username>/', views.user_profile_detail, name='user_profile_detail'),
]