from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status, permissions, filters
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .serializers import UserSerializer, ProfileSerializer, MatchSerializer, PreferenceSerializer
from games_app.serializers import UserGameSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from .models import Profile, Match, Preference
from games_app.models import UserGame
from rest_framework.exceptions import PermissionDenied, NotFound
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Create your views here.

@login_required
def profile(request):
    return render(request, 'users/profile')

class CreateUserView(generics.CreateAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer

  def create(self, request, *args, **kwargs):
    response = super().create(request, *args, **kwargs)
    user = User.objects.get(username=response.data['username'])
    refresh = RefreshToken.for_user(user)
    return Response({
      'refresh': str(refresh),
      'access': str(refresh.access_token),
      'user': response.data
    })

# User Login
class LoginView(APIView):
  permission_classes = [permissions.AllowAny]

  def post(self, request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
      refresh = RefreshToken.for_user(user)
      return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user': UserSerializer(user).data
      })
    return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# User Verification
class VerifyUserView(APIView):
  permission_classes = [permissions.IsAuthenticated]

  def get(self, request):
    user = User.objects.get(username=request.user)  # Fetch user profile
    refresh = RefreshToken.for_user(request.user)  # Generate new refresh token
    return Response({
      'refresh': str(refresh),
      'access': str(refresh.access_token),
      'user': UserSerializer(user).data
    })
  
class ProfilesView(generics.ListAPIView):
   serializer_class = ProfileSerializer

   def get_queryset(self):
      return Profile.objects.all()

   def list(self, request, *args, **kwargs):
      queryset = self.get_queryset()
      profiles_data = ProfileSerializer(queryset, many=True).data

      for profile in profiles_data:
         profile_obj = Profile.objects.get(id=profile['id'])
         user_games = UserGame.objects.filter(profile=profile_obj)
         profile['user_games'] = UserGameSerializer(user_games, many=True).data

      return Response(profiles_data)

  
  
  #Profile View
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
   # lookup_field = 'id'
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
      user = self.request.user
      return Profile.objects.filter(user=user)

    def get_object(self):
        queryset = self.get_queryset()
        obj = generics.get_object_or_404(queryset)
        self.check_object_permissions(self.request, obj)
        return obj
    

class ProfileDetail(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'id'
    permission_classes = [permissions.IsAuthenticated]


class MatchList(generics.ListCreateAPIView):
    serializer_class = MatchSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['user1_profile', 'user2_profile', 'recipricated']

    def get_queryset(self):
        user = self.request.user
        profile = Profile.objects.filter(user=user)
        return Match.objects.filter(Q(user1_profile=profile[0]) | Q(user2_profile=profile[0])).select_related('user1_profile', 'user2_profile')

    def perform_create(self, serializer):
      serializer.save()

class MatchDetail(generics.RetrieveUpdateAPIView):
    serializer_class = MatchSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Get the matched profile ID from the URL
        matched_profile_id = self.kwargs.get('id')

        # Get the profile of the logged-in user
        user_profile = get_object_or_404(Profile, user=self.request.user)

        # Fetch the profile of the matched user
        matched_profile = get_object_or_404(Profile, id=matched_profile_id)

        # Find the Match where one of the profiles is the user's and the other is the matched profile
        match = Match.objects.filter(
            (Q(user1_profile=user_profile) & Q(user2_profile=matched_profile)) |
            (Q(user1_profile=matched_profile) & Q(user2_profile=user_profile))
        ).first()

        if not match:
            raise NotFound(f'No Match found between profile {user_profile.id} and {matched_profile_id}.')

        return match

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

# class MatchDetail(generics.RetrieveUpdateAPIView):
#     serializer_class = MatchSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_object(self):
#         # Get the profile ID from the URL
#         profile_id = self.kwargs.get('id')


#         # Fetch the profile based on ID only
#         profile = get_object_or_404(Profile, id=profile_id)

#         # Find a Match where the given profile is either user1_profile or user2_profile
#         match = Match.objects.filter(
#             Q(user1_profile=profile) | Q(user2_profile=profile)
#         ).first()

#         if not match:
#             raise NotFound('No Match found for the given profile ID.')

#         return match

#     def update(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)

# class MatchDetail(generics.RetrieveUpdateAPIView):
#     serializer_class = MatchSerializer
#     permission_classes = [permissions.IsAuthenticated]
#     lookup_field = 'id'

#     def get_queryset(self):
#         user = self.request.user
#         profile = Profile.objects.filter(user=user)
#         return Match.objects.filter(Q(user1_profile=profile[0]) | Q(user2_profile=profile[0]))


class PreferenceDetail(generics.RetrieveUpdateAPIView):
    serializer_class = PreferenceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        profile = Profile.objects.filter(user=user)
        return Preference.objects.filter(profile=profile[0])

    def get_object(self):
        queryset = self.get_queryset()
        obj = generics.get_object_or_404(queryset)
        self.check_object_permissions(self.request, obj)
        return obj

class OtherPreferenceDetail(generics.RetrieveAPIView):
    serializer_class = PreferenceSerializer
    queryset = Preference.objects.all()
    lookup_field = 'id'
    permission_class = [permissions.IsAuthenticated]
