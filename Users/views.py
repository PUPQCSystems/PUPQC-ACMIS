from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from django.contrib import messages
from django.shortcuts import redirect, render
from .forms import RegistrationForm, LoginForm
from Users.models import NewUser
from django.http import JsonResponse


class UserRegistration(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format='json'):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Redirect to the root URL with a success message
            messages.success(request, 'User is successfully registered!')
            url_landing = "users:landing"
            return JsonResponse({'url_landing': url_landing}, status=200)

        #     return redirect('users:landing')  # Adjust this URL name as needed
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            # Return a validation error using a JSON response
            return JsonResponse({'errors': serializer.errors}, status=400)
    

    # def post(self, request, format='json'):
    #     serializer = UserRegistrationSerializer(data=request.data)
    #     if serializer.is_valid():
    #         user = serializer.save()
    #         if user:
    #             json = serializer.data
    #             return Response(json, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlacklistTokenUpdateView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = ()

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        

def landing_page(request):
    #Getting all the data inside the Program table and storing it to the context variable
    register_form = RegistrationForm()
    records = NewUser.objects.all()

    context = {'records': records, 'register_form': register_form}   
    return render(request, 'users/landing_page.html', context)
    