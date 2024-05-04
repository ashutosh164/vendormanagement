from rest_framework import status, viewsets, generics
from rest_framework.response import Response
from .serializers import *
from django.contrib.auth.models import User
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .models import *
from rest_framework import authentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


class RegisterView(viewsets.ModelViewSet):
    serializer_class = RegisterSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = Response()
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        # request.session['user'] = user

        response.set_cookie(key='token', value=token.key)
        response.set_cookie(key='user', value=user.pk)
        response.set_cookie(key='is_superuser', value=user.is_superuser)
        response.set_cookie(key='username', value=serializer.validated_data['username'])
        response.status_code = status.HTTP_200_OK
        data = {
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'is_superuser': user.is_superuser,
            'username': serializer.validated_data['username']
        }
        response.data = {"Success": "Login successfully", "data": data}
        return response


class VendorView(viewsets.ModelViewSet):
    serializer_class = VendorSerializer
    queryset = Vendor.objects.all()
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [IsAuthenticated]


class PurchaseOrderView(viewsets.ModelViewSet):
    serializer_class = PurchaseOrderSerializer
    queryset = PurchaseOrder.objects.all()
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [IsAuthenticated]


class VendorPerformanceView(generics.RetrieveAPIView):
    queryset = Vendor.objects.all()
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    serializer_class = VendorPerformanceSerializer
    lookup_field = 'id'


@api_view(['POST'])
def acknowledge_purchase_order(request, po_id):
    try:
        po = PurchaseOrder.objects.get(id=po_id)
    except PurchaseOrder.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if po.vendor != request.user:
        return Response(status=status.HTTP_403_FORBIDDEN)

    po.acknowledgment_date = timezone.now()
    po.save()
    po.vendor.update_average_response_time()
    return Response(status=status.HTTP_200_OK)


class PurchaseOrderAcknowledgmentViewSet(generics.UpdateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderAcknowledgmentSerializer
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # print(request.user)
        # if instance.vendor != request.user:
        #     return Response(status=status.HTTP_403_FORBIDDEN)
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        instance.vendor.update_average_response_time()
        return Response(serializer.data)

