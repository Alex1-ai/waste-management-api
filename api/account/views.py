from .serializers import RegisterSerializer, EmailVerificationSerializer,LoginSerializer,ResetPasswordEmailRequestSerializer, SetNewPasswordSerializer, LogoutSerializer
from rest_framework import generics, status, views,permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from .models import User
from .utils import Util
from django.urls import reverse
import jwt

# from mug_api import settings
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from  .renderers import UserRenderer

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import  smart_bytes,smart_str, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.shortcuts import redirect, render
from django.http import HttpResponsePermanentRedirect
import os
class CustomRedirect(HttpResponsePermanentRedirect):
    allowed_schemes=[ os.environ.get('APP_SCHEME'),'http','https']


class RegisterView(generics.GenericAPIView):

    serializer_class = RegisterSerializer
    renderer_classes = (UserRenderer,)

    def post(self, request):
        user = request.data
        print(user)
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print(serializer.data)
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        # print(user)
        token = RefreshToken.for_user(user).access_token
        # print(token)
        # current_site = get_current_site(request).domain
        # relativeLink = reverse('email-verify')
        # absurl = f'http://{current_site}{relativeLink}?token={token}'
        # email_body = 'Hi '+user.username + \
        #     ' Use the link below to verify your email \n' + absurl
        email_body =f"Thank your for creating An Account with us"
        data = {'email_body': email_body, 'to_email': user.email,
                'email_subject': 'Account Successful'}

        Util.send_email(data)
        return Response(user_data, status=status.HTTP_201_CREATED)







class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer

    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        print(token)
        try:
            # print("Entere token")
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            # print(payload)
            user = User.objects.get(id=payload['user_id'])
            # print(user)
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
            # return render(request, "<center><h4> Your account has been successfully activated </h4></center>")
        except jwt.ExpiredSignatureError:
            # print('Token has expired')
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            # print('Invalid token')
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # print('An error occurred:', str(e))
            return Response({'error': 'An unexpected error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    #     except jwt.ExpiredSignatureError as identifier:
    #         return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
    #     except jwt.exceptions.DecodeError as identifier:
    #         return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
    #     except Exception as unexpected_error:
    # # Print or log the unexpected error
    #         print("Unexpected error:", unexpected_error)
    #         return Response({'error': 'An unexpected error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class LoginAPIView(generics.GenericAPIView):
    serializer_class=LoginSerializer
    def post(self, request):
        user=request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)


        return Response(serializer.data, status=status.HTTP_200_OK)



class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class= ResetPasswordEmailRequestSerializer
    def post(self,request):
        serializer = self.serializer_class(data=request.data)

        email = request.data['email']

        if User.objects.filter(email=email).exists():
                user= User.objects.get(email=email)
                uidb64=urlsafe_base64_encode(smart_bytes(user.id))
                token = PasswordResetTokenGenerator().make_token(user)
                current_site = get_current_site(request=request).domain
                relativeLink = reverse('password-reset-confirm', kwargs={'uidb64':uidb64,'token':token})
                redirect_url=request.data.get('redirect_url','')
                absurl = f'http://{current_site}{relativeLink}'
                email_body = 'Hello \n'+ ' Use the link below to reset your email \n' + absurl +'?redirect_url='+redirect_url
                data = {'email_body': email_body, 'to_email': user.email,
                        'email_subject': 'Reset your password'}

                Util.send_email(data)
        # data = {'request':request, 'data': request.data}
        # serializer=self.serializer_class(data=data)
        # serializer.is_valid(raise_exception=True)


        return Response({'success': 'we ave sent you a link to reset your password'}, status=status.HTTP_200_OK)



class PasswordTokenCheckAPI(generics.GenericAPIView):
    def get(self, request,uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            redirect_url = request.GET.get('redirect_url')



            if not PasswordResetTokenGenerator().check_token(user, token):
                if len(redirect_url) >3:
                    return CustomRedirect(redirect_url+"?token_valid=False")
                # return Response({'error':'Token is not valid, please request a new one'}, status=status.HTTP_401_UNAUTHORIZED)
                else:
                    return CustomRedirect(os.environ.get('FRONTEND_URL','')+"?token_valid=False")

            # return Response({'success':True, 'message':'Credential Valid','uidb64':uidb64,'token':token}, status=status.HTTP_200_OK)
            if redirect_url and len(redirect_url) >3:
               return CustomRedirect(redirect_url+"?token_valid=True&?message=Credential Valid&?uidb64="+uidb64+"&?token="+token)
            else :
                return CustomRedirect(os.environ.get('FRONTEND_URL','')+"?token_valid=False")
        except DjangoUnicodeDecodeError :
            if not PasswordResetTokenGenerator().check_token(user):
                return CustomRedirect(redirect_url+"?token_valid=False")
            #   return Response({'error':'Token is not valid, please request a new one'}, status=status.HTTP_401_UNAUTHORIZED)







class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class=SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)


        return Response({'success':True, 'message':'Password reset successfully'},status=status.HTTP_200_OK)



class LogoutAPIView(generics.GenericAPIView):
     serializer_class=LogoutSerializer

     permission_classes=(permissions.IsAuthenticated,)


     def post(self,request):
         serializer = self.serializer_class(data=request.data)
         serializer.is_valid(raise_exception=True)
         serializer.save()

         return Response(status=status.HTTP_204_NO_CONTENT)

class AuthUserAPIView(generics.GenericAPIView):
    permission_classes =(permissions.IsAuthenticated,)


    def get(self, request):
        user = User.objects.get(pk=request.user.pk)
        serializer = RegisterSerializer(user)

        return Response(serializer.data)
# from rest_framework import viewsets
# from rest_framework.permissions import AllowAny
# from .serializers import UserSerializer
# from .models import CustomUser
# from django.http import JsonResponse
# from django.contrib.auth import get_user_model
# from django.views.decorators.csrf import csrf_exempt
# from django.contrib.auth import login, logout
# import re
# # Create your views here.
# import random



# def generate_session_token(length=10):
#     return ''.join(random.SystemRandom().choice([chr(i) for i in range(97,123)]+ [str(i) for i in range(10)]) for _ in range(length))

# @csrf_exempt
# def signin(request):
#     if not request.method == 'POST':
#         return JsonResponse({
#             'error': "send a post request with valid parameters"
#         })
#     print(request)
#     return JsonResponse('ok')
#     # username = request.POST.get('email')
#     # password = request.POST.get('password')

#     # #validate part
#     # if not  re.match("^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", username):
#     #     return JsonResponse({'error': "Enter a valid email"})
#     # MucgEmail = 'mucg.edu.gh'
#     # emailCheck = username.split('@')
#     # if MucgEmail != emailCheck[1].lower():
#     #     print(emailCheck)
#     #     return JsonResponse({"error":"Please Use your school email to register!"})

#     # if len(password) < 7:
#     #     return JsonResponse({'error': 'Password needs to be at least more than 7 characters'})


#     # UserModel = get_user_model()


#     # try:

#     #     user = UserModel.objects.get(email=username)

#     #     if user.check_password(password):
#     #         usr_dict = UserModel.objects.filter(email=username).values().first()
#     #         usr_dict.pop('password')




#     #         if user.session_token != '0':
#     #             user.session_token = "0"
#     #             user.save()
#     #             return JsonResponse({
#     #                 'error': "Previous session exists!"
#     #             })

#     #         token = generate_session_token()
#     #         user.session_token = token
#     #         user.save()
#     #         login(request, user)
#     #         return JsonResponse({
#     #             'token':token,
#     #             'user':usr_dict
#     #         })


#     #     else:
#     #         return JsonResponse({
#     #             'error':"Invalid password"
#     #         })
#     # except UserModel.DoesNotExist:
#     #     return JsonResponse({'error': "Invalid Email"})


# def signout(request,id):
#     logout(request)

#     UserModel = get_user_model()

#     try:
#         user = UserModel.objects.get(pk=id)
#         user.session_token="0"
#         user.save()


#     except UserModel.DoesNotExist:
#         return JsonResponse({'error': "Invalid user ID"})

#     return JsonResponse({'success': 'Logout success'})



# class UserViewSet(viewsets.ModelViewSet):
#     permission_classes_by_action = {'create':[AllowAny]}

#     queryset = CustomUser.objects.all().order_by('id')
#     serializer_class = UserSerializer


#     def get_permissions(self):
#         try:
#             return [permission() for permission in self.permission_classes_by_action[self.action]]
#         except KeyError:
#             return [permission() for permission in self.permission_classes]