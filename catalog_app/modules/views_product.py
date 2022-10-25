from datetime import datetime
from django.shortcuts import render, resolve_url, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth import login, logout
from rest_framework import generics, status, viewsets, status, viewsets, permissions, renderers
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.decorators import api_view, action, permission_classes, authentication_classes
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter, SearchFilter
# from django_filter import FilterSet
# from ..models.product_model import Product
from ..models.catalog_model import (Product, Category)
from ..apis import product_ws
from ..serializers.product_serializer import ProductSerializer
import json
from django.views.decorators.csrf import csrf_exempt


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @authentication_classes([TokenAuthentication])
def GetProductInfo(request):
    return product_ws.GetProductInfo(request)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @authentication_classes([TokenAuthentication])
@csrf_exempt
def AddProduct(request):
    print('into AddProduct')
    return product_ws.AddProduct(request)


class ProductInfoViewSet(viewsets.ModelViewSet):
    # authentication_classes = TokenAuthentication  # Token access
    permission_classes = [IsAuthenticated]  # Basic Auth
    queryset = Product.objects.filter(active=True).order_by('created_at')
    serializer_class = ProductSerializer
    # http_method_names = ['get', 'post', 'put', 'patch', 'head', 'delete']
    # swagger_schema = None

    def get_permissions(self):
        if self.action == 'list':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def filter_queryset(self, queryset):
        # queryset = self.queryset.filter(username=request.data.username)
        _id = self.request.user.id
        if _id:
            queryset = self.queryset.filter(user_id=_id)
            return queryset
        return self.queryset

    @action(methods=['POST'], detail=True)
    def update_product(self, request, pk):
        print('Class ViewSet [POST]: UpdateProduct pk = ', pk)
        return product_ws.UpdateProduct(request, pk)

    def get(self, request, pk, *args, **kwargs):
        # queryset = Product.objects.filter(id=pk, user_id=request.user.id, active=True)
        print('Class ViewSet [GET] for /catalog/product/' + pk + '/update_product/')
        from pprint import pprint;
        pprint(self.serializer_class)
        return product_ws.GetProductInfoDetail(request, pk)


class CreateProduct(CreateModelMixin, GenericAPIView):
    serializer_class = ProductSerializer
    # authentication_classes = TokenAuthentication  # Token access
    permission_classes = [IsAuthenticated]          # Basic Auth

    def post(self, request, *args, **kwargs):
        print(self.request.data)
        # print(self.request.data.get("content"))
        return self.create(request, *args, **kwargs)
        # return HttpResponse('ok POST')

    # def perform_create(self, serializer):
    #    _id = self.request.data.get('id')
    #    comment = get_object_or_404(Profile, pk=_id)
    #    print(comment)

    # def get(self, request, *args, **kwargs):
    #     return HttpResponse('ok GET')


# Get all
# class ListAllProfile(ListAPIView):
#     queryset = Profile.objects.all()
#     serializer_class = User_appSerializer
#     permission_classes = [IsAuthenticated]


# class CreateProfile(CreateModelMixin, GenericAPIView):
#     serializer_class = UserSerializer
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request, *args, **kwargs):
#         # print(self.request.data)
#         # print(self.request.data.get("name"))
#         return self.create(request, *args, **kwargs)
#
#     # def perform_create(self, serializer):
#     #    _id = self.request.data.get('id')
#     #    comment = get_object_or_404(Profile, pk=_id)
#     #    print(comment)

def index(request):
    # profile = request.session.get('profile') # print("____: "+json.dumps(profile)+profile['first_name'] )
    print('Product: Run debug ok')
    if request.user.is_authenticated:
        return HttpResponse('Webcome to HDWebshoft') # return redirect('user:home')
    return render(request, "index_catalog.html",
                  {
                      'title': "Index page",
                      # 'next':'/home/',
                      'content': "Example app page for Django.",
                      'year': datetime.now().year,
                      'design': "Hà Huy Hoàng"
                  }
                  )