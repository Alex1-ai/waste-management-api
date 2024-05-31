from django.conf import settings
from rest_framework import generics, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Trash
from .serializers import TrashSerializer
from ..account.utils import Util

class TrashListCreateView(generics.ListCreateAPIView):
    serializer_class = TrashSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Trash.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        trash_instance = serializer.save(user=self.request.user)
        # Send email notification to the admin
        admin_email = settings.ADMIN_EMAIL  # Replace with your admin email
        subject = "New Trash Takeout Order"
        message = f"A new trash takeout order has been placed.\n\n"
        message += f"User: {trash_instance.user.username}\n"
        message += f"Email: {trash_instance.user.email}\n"
        message += f"Contact: {trash_instance.contact}\n"
        message += f"Location: {trash_instance.location}\n"
        message += f"Take Out Date: {trash_instance.take_out_date}\n"

        email_body =f"{message}"
        data = {'email_body': email_body, 'to_email': admin_email,
                'email_subject': subject}

        Util.send_email(data)



class TrashDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TrashSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Trash.objects.filter(user=self.request.user)










# from django.shortcuts import render
# from .serializers import TrashSerializer
# from django.core.mail import send_mail
# from django.conf import settings
# from rest_framework import generics, permissions
# from rest_framework.response import Response
# from rest_framework_simplejwt.authentication import JWTAuthentication
# # Create your views here.
# class TrashView(generics.GenericAPIView):
#     serializer_class = TrashSerializer
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [permissions.IsAuthenticated]


#     def post(self, request):
#         print(request)
#         trash = request.data
#         print(trash)
#         # serializer = self.serializer_class(data=trash)
#         # serializer.is_valid(raise_exception=True)
#         # serializer.save()
#         # user_data = serializer.data
#         # user = User.objects.get(email=user_data['email'])
#         # # print(user)
#         # token = RefreshToken.for_user(user).access_token
#         # # print(token)
#         # current_site = get_current_site(request).domain
#         # relativeLink = reverse('email-verify')
#         # absurl = f'http://{current_site}{relativeLink}?token={token}'
#         # email_body = 'Hi '+user.username + \
#         #     ' Use the link below to verify your email \n' + absurl
#         # data = {'email_body': email_body, 'to_email': user.email,
#         #         'email_subject': 'Verify your email'}

#         # Util.send_email(data)
#         # return Response(user_data, status=status.HTTP_201_CREATED)
#         return Response({"message":"success"})