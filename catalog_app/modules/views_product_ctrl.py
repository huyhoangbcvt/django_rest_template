from django.shortcuts import render, resolve_url, redirect, get_object_or_404
# from ..models.product_model import Product
from django.core.paginator import Paginator

from django.db.models import Count, F, Value, Func
from django.db.models.functions import Length, Upper
from django.db.models.lookups import GreaterThan
from django.db.models import OuterRef, Subquery
from .forms_product_ctrl import ProductForm

from django.http import (HttpResponse, HttpResponseRedirect)
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.core.files.base import ContentFile
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from ..models.catalog_model import Category, Product
from django.views.generic import (
    FormView, UpdateView, View
)
from datetime import datetime


def product_list(request):
    # auth cho func, using LoginRequiredMixin cho class
    if not request.user.is_authenticated:
        return redirect('user:login')
    # pm = Product.objects.all()
    # sort pm = Product.objects.order_by(F('created_at').desc(nulls_last=True)) #.asc()
    # filter
    user = request.user
    # print(user.username)
    # queryset
    pm = Product.objects.filter(user_id=user.id).order_by(F('created_at').desc(nulls_last=True))
    paginator = Paginator(pm, 2)  # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'product/product_list.html', {'page_obj': page_obj})


class AddProduct(TemplateView, LoginRequiredMixin):
    form = ProductForm
    template_name = 'product/product_form.html'

    def post(self, request, *args, **kwargs):
        user = request.user
        # if user is not None and user.is_superuser:
        #     user = User.objects.all()
        form = ProductForm(request.POST, request.FILES, user=request.user)  # , user=request.user, product=pm
        if form.is_valid():
            obj = form.save()
            return HttpResponseRedirect(reverse_lazy('catalog:product_detail', kwargs={'pk': obj.id}))

        context = self.get_context_data(form=form)
        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class ProductDisplay(DetailView, LoginRequiredMixin):
    model = Product
    template_name = 'product/product_detail.html'
    context_object_name = 'UF'


class ChangeProduct(UpdateView):
    queryset = Product.objects.all()
    profile_form_class = ProductForm
    success_url = reverse_lazy('catalog:products')
    template_name = "product/product_change.html"
    add_home = False
    extra_context = {
        'title': "Thay đổi thông tin cá nhân",
        'year': datetime.now().year
    }

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated is None:
            return render(request, 'registration/login.html')
        # self.extra_context['user_form'] = UserForm(instance=request.user)  # user_form = self.user_form_class(None)
        self.extra_context['product_form'] = ProductForm(instance=self.get_object())
        # and then just pass them to my template
        return render(request, self.template_name, self.extra_context)  # {'user_form': user_form, 'profile_form': profile_form}

    # def get_object(self, *args, **kwargs):
    #     product_to_edit = get_object_or_404(Product, pk=self.kwargs['pk'])
    #     return product_to_edit

    def post(self, request, *args, **kwargs):
        # if request.POST:
        form = ProductForm(request.POST, request.FILES, instance=self.get_object(), user=request.user)
        if form.is_valid():
            # print(form)
            form.save()
            return redirect('catalog:products')

        context = self.get_context_data(form=form)
        return self.render_to_response(context)

        # else: # form not valid - each form will contain errors in form.errors
        # return render(request, self.template_name, {
        #     # 'user_form': user_form,
        #     'product_form': ProductForm
        # })

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy("catalog:products")
