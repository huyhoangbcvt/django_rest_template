from datetime import datetime
from django.shortcuts import render, resolve_url, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth import login, logout
from rest_framework import generics, status, viewsets, status, viewsets, permissions, renderers
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.decorators import api_view, action, permission_classes, authentication_classes, renderer_classes
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
# from django_filter import FilterSet
from ..apis import category_ws
from ..serializers.category_serializer import CategorySerializer
from ..serializers.contact_serializer import ContactSerializer
# from ..models.category_model import Category
from ..models.catalog_model import (Product, Category, Contact)
from django.views.decorators.csrf import csrf_exempt
from ..util.pagination import BasePagination


@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @authentication_classes([TokenAuthentication]) # @renderer_classes([JSONRenderer])
def GetCategoryInfo(request):
    print('Func GET: GetCategoryInfo')
    return category_ws.GetCategoryInfo(request)


@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Basic Auth
# @authentication_classes([TokenAuthentication])
@csrf_exempt
def AddCategory(request):
    print('Func POST: AddCategory')
    return category_ws.AddCategory(request)


class CategoryInfoViewSet(viewsets.ModelViewSet):
    # authentication_classes = TokenAuthentication  # Token access
    permission_classes = [IsAuthenticated]  # Basic Auth
    queryset = Category.objects.filter(active=True).order_by('created_at')
    serializer_class = CategorySerializer
    pagination_class = BasePagination
    # http_method_names = ['get', 'post', 'put', 'patch', 'head', 'delete']
    # swagger_schema = None
    charset = 'UTF-8'

    def get_permissions(self):
        if self.action == 'list':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    @action(methods=['PATCH'], detail=True, url_path='active', url_name='active')
    def active_category(self, request, pk):
        print('Class ViewSet [PATCH]: active_category pk = ', pk)
        return category_ws.UpdateActiveCategory(request, pk, _active=True)

    @action(methods=['PATCH'], detail=True, url_path='unactive', url_name='unactive')
    def un_active_category(self, request, pk):
        print('Class ViewSet [PATCH]: un_active_category pk = ', pk)
        return category_ws.UpdateActiveCategory(request, pk, _active=False)

    # def filter_queryset(self, queryset):
    #     # queryset = self.queryset.filter(username=request.data.username)
    #     _id = self.request.user.id
    #     if _id:
    #         queryset = self.queryset.filter(user_id=_id)
    #         return queryset
    #     return self.queryset

    # def get(self, request, pk, *args, **kwargs):
    #     print('Class ViewSet [GET] for /catalog/category/'+pk+'/update_category/')
    #     return category_ws.GetCategoryInfoDetail(request, pk)


class CreateCategory(CreateModelMixin, GenericAPIView):
    serializer_class = CategorySerializer
    # authentication_classes = TokenAuthentication  # Token access
    permission_classes = [IsAuthenticated]          # Basic Auth

    def post(self, request, *args, **kwargs):
        print(self.request.data)
        print(self.request.data.get("user"))
        return self.create(request, *args, **kwargs)
        # return HttpResponse('ok POST')

    # def perform_create(self, serializer):
    #    _id = self.request.data.get('id')
    #    comment = get_object_or_404(Profile, pk=_id)
    #    print(comment)


# Neu dung ViewSet ko phai ModelViewSet thi phai tu lam GET, POST, DETAIL, PUT, PATH, DELETE
class CreateContactViewSet(viewsets.ViewSet):
    # authentication_classes = TokenAuthentication  # Token access
    permission_classes = [IsAuthenticated]  # Basic Auth
    queryset = Contact.objects.all().order_by('-date_joined')
    serializer_class = ContactSerializer
    # http_method_names = ['get', 'post', 'put', 'patch', 'head', 'delete']
    # swagger_schema = None
    charset = 'UTF-8'

    def get_permissions(self):
        if self.action == 'list':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def list(self, request):  # GET
        print('GET list')
        queryset = Contact.objects.all().order_by('-date_joined')
        serializer = ContactSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):  # POST
        print('POST create')
        return HttpResponse('POST create done')

    def retrieve(self, request, pk=None):  # Detail  GET co param id
        print('GET')
        return HttpResponse('GET Detail done')

    def update(self, request, pk=None):  # PUT
        print('PUT')
        return HttpResponse('PUT update done')

    def partial_update(self, request, pk=None):  # PATH update 1 phan
        print('PATH')
        return HttpResponse('PATH partial_update 1 phan done')

    def destroy(self, request, pk=None):  # Delete
        print('DELETE')
        return HttpResponse('DELETE destroy done')

    # def post(self, request, *args, **kwargs):
    #     print(self.request.data)
    #     return self.create(request, *args, **kwargs)


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