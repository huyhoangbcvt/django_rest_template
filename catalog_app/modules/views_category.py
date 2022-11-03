from datetime import datetime
from django.shortcuts import render, resolve_url, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count, F, Value, Func

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
from ..serializers.category_serializer import CategorySerializer, CategoryAddSerializer
from ..serializers.product_serializer import ProductSerializer
# from ..serializers.contact_serializer import ContactSerializer
# from ..models.category_model import Category
from ..models.catalog_model import (Product, Category)
from ..util.pagination import BasePagination
from ..util.error_code import ErrorInCode


@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @authentication_classes([TokenAuthentication]) # @renderer_classes([JSONRenderer])
def GetCategoryInfo(request):
    print('Func GET: GetCategoryInfo')
    return category_ws.getCategoryInfo(request)


@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Basic Auth
# @authentication_classes([TokenAuthentication])
@csrf_exempt
def AddCategory(request):
    print('Func POST: AddCategory')
    return category_ws.addCategory(request)


class CategoryViewSet(viewsets.ModelViewSet):
    # authentication_classes = TokenAuthentication  # Token access
    permission_classes = [IsAuthenticated]  # Basic Auth
    queryset = Category.objects.filter(active=True).select_related("user").order_by('-created_at')
    serializer_class = CategorySerializer
    pagination_class = BasePagination
    # http_method_names = ['get', 'post', 'put', 'patch', 'head', 'delete']
    # swagger_schema = None
    charset = 'UTF-8'

    def get_permissions(self):
        print(self.action)
        if self.action == 'list':
            return [permissions.AllowAny()]
        if self.action == 'create':
            self.serializer_class = CategoryAddSerializer
            return [permissions.IsAuthenticated()]
        if self.action == 'active_product':
            return [permissions.IsAuthenticated()]
        if self.action == 'un_active_product':
            return [permissions.IsAuthenticated()]
        if self.action == 'add_comment':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated()]

    def create(self, request, *args, **kwargs):  # POST
        if request.user:
            # return category_ws.addCategory(request)
            serializer = self.serializer_class(data=request.data)
            try:
                # serializer.is_valid(raise_exception=True)
                if serializer.is_valid():
                    response = serializer.save(request)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            except ErrorInCode as e:
                return Response(e, status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.validated_data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):
        if request.user == self.get_object().user:
            return super().destroy(request, *args, **kwargs)
        return Response(status=status.HTTP_403_FORBIDDEN)

    @action(methods=['PATCH'], detail=True, url_path='active', url_name='active')
    def active_category(self, request, pk):
        print('Category ViewSet ['+self.action+']: active_category pk = ', pk)
        return category_ws.updateActiveCategory(request, pk, _active=True)

    @action(methods=['PATCH'], detail=True, url_path='un-active')
    def un_active_category(self, request, pk):
        print('Category ViewSet ['+self.action+']: un_active_category pk = ', pk)
        return category_ws.updateActiveCategory(request, pk, _active=False)

    @action(methods=['get'], detail=True, url_path='products')
    def get_products(self, request, pk):
        print('Category ViewSet : get_products pk = ', pk)
        # category = Category.objects.get(pk=pk)
        # products = category.products.filter(active=True)
        products = self.get_object().products.filter(active=True)
        kw_param = self.request.query_params.get('p_name')
        if kw_param is not None:
            products = products.filter(name__icontains=kw_param)
        # category_count_products = products.annotate(products_count=Count('products'))\
        #     .values("id", "name", "products_count")
        # print(category_count_products[0]['products_count'])
        return Response(ProductSerializer(products, many=True).data, status=status.HTTP_200_OK)

    def get_queryset(self):
        categories = self.queryset
        ca_name = self.request.query_params.get('ca_name')
        if ca_name is not None:
            categories = categories.filter(name__icontains=ca_name)

        # p_id = self.request.query_params.get('product_id')
        # if p_id is not None:
        #     categories = categories.filter(product_id=p_id)
        return categories

    # def filter_queryset(self, queryset):
    #     self.queryset = self.get_object()
    #     queryset = self.queryset.filter(username=request.data.username)
    #     if self.request.user:
    #         queryset = self.queryset.filter(user_id=self.request.user.id)
    #         return queryset
    #     return self.queryset


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
# class ContactViewSet(viewsets.ViewSet):
#     # authentication_classes = TokenAuthentication  # Token access
#     permission_classes = [IsAuthenticated]  # Basic Auth
#     queryset = Contact.objects.all().order_by('-date_joined')
#     serializer_class = ContactSerializer
#     # http_method_names = ['get', 'post', 'put', 'patch', 'head', 'delete']
#     # swagger_schema = None
#     charset = 'UTF-8'
#
#     def get_permissions(self):
#         if self.action == 'list':
#             return [permissions.AllowAny()]
#         return [permissions.IsAuthenticated()]
#
#     def list(self, request):  # GET
#         print('GET list')
#         queryset = Contact.objects.all().order_by('-date_joined')
#         serializer = ContactSerializer(queryset, many=True)
#         return Response(serializer.data)
#
#     def create(self, request):  # POST
#         print('POST create')
#         return HttpResponse('POST create done')
#
#     def retrieve(self, request, pk=None):  # Detail  GET co param id
#         print('GET')
#         return HttpResponse('GET Detail done')
#
#     def update(self, request, pk=None):  # PUT
#         print('PUT')
#         return HttpResponse('PUT update done')
#
#     def partial_update(self, request, pk=None):  # PATH update 1 phan
#         print('PATH')
#         return HttpResponse('PATH partial_update 1 phan done')
#
#     def destroy(self, request, pk=None):  # Delete
#         print('DELETE')
#         return HttpResponse('DELETE destroy done')
#
#     # def post(self, request, *args, **kwargs):
#     #     print(self.request.data)
#     #     return self.create(request, *args, **kwargs)


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