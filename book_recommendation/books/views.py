import requests
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from dotenv import load_dotenv
import os
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect
from .models import Recommendation
from .serializers import RecommendationSerializer, CommentSerializer,RegisterSerializer,LoginSerializer,FilterSerializer
from .forms import RegisterForm, LoginForm,RecommendationForm
import random

GOOGLE_BOOKS_API_KEY = os.getenv('GOOGLE_BOOKS_API_KEY')
GOOGLE_BOOKS_API_URL = 'https://books.googleapis.com/books/v1/volumes'

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

token_param = openapi.Parameter(
    'Authorization',
    openapi.IN_HEADER,
    description="Bearer [your-token] or Token [your-token]",
    type=openapi.TYPE_STRING,
    required=True,
)



# Helper function to get JWT tokens
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def home_view(request):
    return render(request, 'home.html')


# User registration
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm.RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            response = redirect('index')
            return response
    else:
        form = RegisterForm.RegisterForm()
    return render(request, 'register.html', {'form': form})

# User login with JWT token generation
def login_view(request):
    if request.method == 'POST':
        form = LoginForm.LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            tokens = get_tokens_for_user(user)
            response = redirect('index')
            response.set_cookie('jwt_access', tokens['access'], httponly=True)
            response.set_cookie('jwt_refresh', tokens['refresh'], httponly=True)
            return response
    else:
        form = LoginForm.LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def index_view(request):
    return render(request, 'index.html')

def logout_view(request):
    auth_logout(request)
    response = redirect('home')
    response.delete_cookie('jwt_access')
    response.delete_cookie('jwt_refresh')
    return response


def search_books(request):
    query = request.GET.get('q', '')
    books = []
    
    if query:
        params = {
            'q': query,
            'key': GOOGLE_BOOKS_API_KEY,
            'maxResults': 10 
        }
        
        response = requests.get(GOOGLE_BOOKS_API_URL, params=params)
        
        if response.status_code == 200:
            items = response.json().get('items', [])
            books = [{
                'title': book['volumeInfo'].get('title', ''),
                'author': ', '.join(book['volumeInfo'].get('authors', [])),
                'description': book['volumeInfo'].get('description', ''),
                'cover_image': book['volumeInfo'].get('imageLinks', {}).get('thumbnail', ''),
                'rating': book['volumeInfo'].get('averageRating', 0)
            } for book in items]
    
    return render(request, 'search.html', {'books': books})


@login_required
def submit_recommendation_view(request):
    if request.method == 'POST':
        form = RecommendationForm.RecommendationForm(request.POST)
        if form.is_valid():
            recommendation = form.save(commit=False)
            recommendation.user = request.user
            recommendation.save()
            return redirect('index')
    else:
        form = RecommendationForm.RecommendationForm()
    return render(request, 'submit_recommendation.html', {'form': form})


@login_required
def view_recommendations(request):
    recommendations = list(Recommendation.objects.all())
    if len(recommendations) > 10:
        recommendations = random.sample(recommendations, 10)
    context = {'recommendations': recommendations}
    return render(request, 'view_recommendations.html', context)


#-------------------API ENDPOINTS FOR FRONTEND LIBRARIES-----------------------------------------------------

#For Internal Use Only
@api_view(['POST'])
def obtain_jwt_token(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    if user:
        tokens = get_tokens_for_user(user)
        return Response(tokens, status=status.HTTP_200_OK)
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)



@swagger_auto_schema(
    method='post',
    request_body=RegisterSerializer,
    responses={201: 'User registered successfully', 400: 'Bad request'}
)
@api_view(['POST'])
def register_user(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@swagger_auto_schema(
    method='post',
    request_body=LoginSerializer,
    responses={200: 'User logged in successfully', 401: 'Invalid credentials'}
)
@api_view(['POST'])
def login_user(request):
    serializer = LoginSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)



@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter('q', openapi.IN_QUERY, description="Search query", type=openapi.TYPE_STRING)
    ],
    responses={200: 'Books retrieved successfully', 500: 'Internal server error'}
)
@api_view(['GET'])
def search_books_api(request):
    query = request.GET.get('q', '')
    books = []
    
    if query:
        params = {
            'q': query,
            'key': GOOGLE_BOOKS_API_KEY,
            'maxResults': 20 #LIMITED TO 10
        }
        
        try:
            response = requests.get(GOOGLE_BOOKS_API_URL, params=params)
            response.raise_for_status()  
            items = response.json().get('items', [])
            books = [{
                'title': book['volumeInfo'].get('title', ''),
                'author': ', '.join(book['volumeInfo'].get('authors', [])),
                'description': book['volumeInfo'].get('description', ''),
                'cover_image': book['volumeInfo'].get('imageLinks', {}).get('thumbnail', ''),
                'rating': book['volumeInfo'].get('averageRating', 0)
            } for book in items]
        except requests.RequestException as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return Response({'books': books}, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='get',
    manual_parameters=[token_param],
    responses={200: RecommendationSerializer(many=True), 401: 'Unauthorized'}
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_recommendations(request):
    recommendations = Recommendation.objects.all()
    serializer = RecommendationSerializer(recommendations, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)



@swagger_auto_schema(
    method='post',
    manual_parameters=[token_param],
    request_body=RecommendationSerializer,
    responses={201: RecommendationSerializer, 400: 'Bad request'}
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_recommendation(request):
    serializer = RecommendationSerializer(data=request.data)
    
    if serializer.is_valid():
        recommendation = serializer.save(user=request.user)
        return Response(RecommendationSerializer(recommendation).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@swagger_auto_schema(
    method='post',
    manual_parameters=[token_param],
    request_body=CommentSerializer,
    responses={201: 'Comment has been added', 400: 'Bad request'}
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def make_comment(request):
    serializer = CommentSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save() 
        return Response({'message': 'Comment has been added'}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@swagger_auto_schema(
    method='patch',
    manual_parameters=[token_param],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'recommendation': openapi.Schema(type=openapi.TYPE_INTEGER, description='Recommendation ID'),
        }
    ),
    responses={200: 'Recommendation has been liked', 400: 'Bad request', 404: 'Recommendation not found'}
)
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def like_recommendations(request):
    recommendation_id = request.data.get('recommendation')
    
    if not recommendation_id:
        return Response({'error': 'Recommendation ID is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        recommendation = Recommendation.objects.get(id=recommendation_id)
        recommendation.like_count += 1
        recommendation.save()
        return Response({'message': 'Recommendation has been liked'}, status=status.HTTP_200_OK)
    
    except Recommendation.DoesNotExist:
        return Response({'error': 'Recommendation not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    

@swagger_auto_schema(
    method='get',
    manual_parameters=[token_param],
    query_serializer=FilterSerializer,
    responses={200: RecommendationSerializer(many=True), 400: 'Bad request', 401: 'Unauthorized'}
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def filter_recommendations(request):
    serializer = FilterSerializer(data=request.GET)
    
    if serializer.is_valid():
        rating = serializer.validated_data.get('rating')
        publication_date = serializer.validated_data.get('publication_date')
        sort_by = serializer.validated_data.get('sort_by', 'publication_date')
        
        recommendations = Recommendation.objects.all()
        
        if rating is not None:
            recommendations = recommendations.filter(rating__gte=rating)
        
        if publication_date is not None:
            recommendations = recommendations.filter(publication_date=publication_date)
        
        if sort_by:
            recommendations = recommendations.order_by(sort_by)
        
        response_serializer = RecommendationSerializer(recommendations, many=True)
        return Response(response_serializer.data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)