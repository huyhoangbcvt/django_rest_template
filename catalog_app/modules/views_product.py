from datetime import datetime
from django.shortcuts import render, resolve_url, redirect
from django.http import HttpResponse
from django.db.models import Count, F, Value, Func
import json
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth import login, logout
from rest_framework import generics, status, viewsets, mixins, status, viewsets, permissions, renderers
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
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
from ..serializers.product_serializer import ProductSerializer, ProductAddSerializer
from ..serializers.category_serializer import CategorySerializer
from ..util.pagination import BasePagination
from ..util.error_code import ErrorInCode


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @authentication_classes([TokenAuthentication])
def GetProductInfo(request):
    return product_ws.getProductInfo(request)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @authentication_classes([TokenAuthentication])
@csrf_exempt
def AddProduct(request):
    print('into AddProduct')
    return product_ws.addProduct(request)


class ProductViewSet(viewsets.ViewSet,
                     generics.CreateAPIView,
                     generics.DestroyAPIView,
                     generics.ListAPIView,
                     generics.RetrieveUpdateAPIView,
                     generics.UpdateAPIView):  # viewsets.ModelViewSet
    # authentication_classes = TokenAuthentication  # Token access
    permission_classes = [IsAuthenticated]  # Basic Auth
    queryset = Product.objects.filter(active=True).select_related('user').order_by('-created_at')
    serializer_class = ProductSerializer
    pagination_class = BasePagination
    # http_method_names = ['get', 'post', 'put', 'patch', 'head', 'delete']
    # swagger_schema = None

    def get_permissions(self):
        # print(self.action)
        if self.action == 'list':
            return [permissions.AllowAny()]
        if self.action == 'create':
            self.serializer_class = ProductAddSerializer
            return [permissions.IsAuthenticated()]
        if self.action == 'active_product':
            return [permissions.IsAuthenticated()]
        if self.action == 'un_active_product':
            return [permissions.IsAuthenticated()]
        if self.action == 'add_comment':
            return [permissions.IsAuthenticated()]
        if self.action == 'add_contact':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated()]

    def create(self, request, *args, **kwargs):  # POST
        if request.user:
            serializer = self.serializer_class(data=request.data)
            try:
                # serializer.is_valid(raise_exception=True)
                if serializer.is_valid():
                    # categories = request.data.get('categories')
                    # print(categories)
                    response = serializer.save(request)
                    return Response(status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            except ErrorInCode as e:
                return Response(e, status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.validated_data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_403_FORBIDDEN)
        # if request.user:
        #     return super().create(request, *args, **kwargs)
        # return Response(status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):
        if request.user == self.get_object().user:
            return super().destroy(request, *args, **kwargs)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def update(self, request, *args, **kwargs):
        if request.user == self.get_object().user:
            return super().update(request, *args, **kwargs)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def partial_update(self, request, *args, **kwargs):
        if request.user == self.get_object().user:
            return super().partial_update(request, *args, **kwargs)
        return Response(status=status.HTTP_403_FORBIDDEN)

    @action(methods=['post'], detail=True, url_path='active', url_name='active')
    def active_product(self, request, pk):
        print('Product ViewSet ['+self.action+']: active_product pk = ', pk)
        return product_ws.updateActiveProduct(request, pk, _active=True)

    @action(methods=['post'], detail=True, url_path='un-active')
    def un_active_product(self, request, pk):
        print('Product ViewSet : un_active_product pk = ', pk)
        return product_ws.updateActiveProduct(request, pk, _active=False)

    @action(methods=['post'], detail=True, url_path='add-comment')
    def add_comment(self, request, pk):
        print('Product ViewSet [' + self.action + ']: add_comment pk = ', pk)
        # return HttpResponse('PUT U  pdate Detail done')
        return product_ws.addCommentProduct(self, request)

    @action(methods=['get'], detail=True, url_path='categories')
    def get_categories(self, request, pk):
        print('Product ViewSet : get_categories pk = ', pk)
        # categories = Category.objects.filter(active=True)
        # product = Product.objects.get(pk=pk, active=True)
        _product = Product.objects.filter(id=pk, active=True)
        # ds = self.get_object().categories.through
        # print(ds)
        product_count_categories = _product.annotate(categories_count=Count('categories')).values("id", "name", "categories_count")
        print(product_count_categories[0]['categories_count'])
        category_related = Category.objects.prefetch_related('products')
        categories = []
        for category in category_related:
            # categories.append(category)
            products = [product.name for product in category.products.filter(id=pk)]
            if products:
                categories.append({'id': category.id, 'name': category.name, 'products': products, 'categories_count': product_count_categories[0]['categories_count']})
        return Response(categories, status=status.HTTP_200_OK)
        # return Response(CategorySerializer(categories, many=True).data, status=status.HTTP_200_OK)

    def get_queryset(self):
        products = self.queryset
        p_name = self.request.query_params.get('p_name')
        if p_name is not None:
            products = products.filter(name__icontains=p_name)

        # ca_id = self.request.query_params.get('category_id')
        # if ca_id is not None:
        #     products = products.filter(category_id=ca_id)
        return products

    # def filter_queryset(self, queryset):
    #     self.queryset = self.get_object()
    #     queryset = self.queryset.filter(username=request.data.username)
    #     if self.request.user:
    #         queryset = self.queryset.filter(user_id=self.request.user.id)
    #         return queryset
    #     return self.queryset

    # @action(methods=['post'], detail=True, url_path='add-contact')
    # def add_contact(self, request, pk):
    #     self.queryset = self.get_object()
    #     print('Product ViewSet [' + self.action + ']: add_contact pk = ', pk)
    #     # return Response(status=status.HTTP_201_CREATED)
    #     return product_ws.addContactProduct(self, request)


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
                  })
