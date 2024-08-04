from django.urls import path
from .views import (
    search_books, register_view,home_view, login_view,index_view,logout_view,submit_recommendation_view,view_recommendations,
    obtain_jwt_token,make_comment,like_recommendations,filter_recommendations,submit_recommendation,get_recommendations,
    register_user,login_user,search_books_api
)
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Book Bank",
        default_version='v1',
        description="Documentation for Book Bank API's",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="sanchitahujafas@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=[],
)

urlpatterns = [
    path('', home_view, name='home'),
    path('search/', search_books, name='search_books'),
    path('register/', register_view, name='registerview'),
    path('index/', index_view, name='index'),
    path('login/', login_view, name='loginview'),
    path('logout/', logout_view, name='logout'),
    path('submit_recommendations/', submit_recommendation_view, name='submit_recommendation_view'),
    path('view_recommendations/', view_recommendations, name='view_recommendations'),
    
    path('submit_recommendation/', submit_recommendation, name='submit_recommendation'),
    path('get_recommendation/', get_recommendations, name='submit_recommendation'),
    path('token/', obtain_jwt_token, name='obtain_token'),
    path('comment/',make_comment,name='comment'),
    path('like/',like_recommendations,name='like'),
    path('filter/',filter_recommendations,name='filter'),
    path('registeruser/', register_user, name='register'),
    path('loginuser/', login_user, name='login'),
    
    path('searchbooks/',search_books_api,name='searchbooks'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api-json/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]
