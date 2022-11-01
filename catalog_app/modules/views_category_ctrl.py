from django.shortcuts import render, resolve_url, redirect, get_object_or_404
from django.core.paginator import Paginator

from django.db.models import Count, F, Value, Func
from django.db.models.functions import Length, Upper
from django.db.models.lookups import GreaterThan
from django.db.models import OuterRef, Subquery
from .forms_category_ctrl import CatalogForm

from django.http import (HttpResponse, HttpResponseRedirect)
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.core.files.base import ContentFile
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# from ..models.product_model import Product
# from ..models.category_model import Category
from ..models.catalog_model import Category, Product
from django.views.generic import (
    FormView, UpdateView, View
)
from datetime import datetime


# auth cho func, using LoginRequiredMixin cho class
@login_required()
def category_list(request):
    # pm = Category.objects.all()
    # sort pm = Category.objects.order_by(F('created_at').desc(nulls_last=True)) #.asc()
    # filter
    user = request.user
    # print(user.username)
    pm = Category.objects.filter(user_id=user.id).order_by(F('created_at').desc(nulls_last=True))
    # queryset
    paginator = Paginator(pm, 2)  # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'category/category_list.html', {'page_obj': page_obj})


class AddCategory(TemplateView, LoginRequiredMixin):
    # form = CatalogForm
    # template_name = 'blog/upload_category.html'

    def post(self, request, *args, **kwargs):
        user = request.user
        # print(user.username)
        pm = Product.objects.filter(user_id=user.id).order_by(F('created_at').desc(nulls_last=True))
        # from pprint import pprint;pprint(pm)
        form = CatalogForm(request.POST, request.FILES, user=user, product=pm) #, user=request.user, product=pm
        if form.is_valid():
            obj = form.save()
            return HttpResponseRedirect(reverse_lazy('catalog:category_detail', kwargs={'pk': obj.id}))

        context = self.get_context_data(form=form)
        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        user = request.user
        # print(user.username)
        pm = Product.objects.filter(user_id=user.id).order_by(F('created_at').desc(nulls_last=True))
        # from pprint import pprint;pprint(pm)
        form = CatalogForm(request.POST, request.FILES, user=user, product=pm)  # , user=request.user, product=pm
        return render(request, 'category/category_form.html', {'form': form})
        # return self.post(request, *args, **kwargs)


# Upload template
class CategoryDisplay(DetailView, LoginRequiredMixin):
    model = Category
    template_name = 'category/category_detail.html'
    context_object_name = 'UF'


class ChangeCategory(UpdateView):
    queryset = Category.objects.all()
    profile_form_class = CatalogForm
    success_url = reverse_lazy('catalog:categories')
    template_name = "category/category_change.html"
    add_home = False
    extra_context = {
        'title': "Thay đổi Category",
        'year': datetime.now().year
    }

    def get_form_kwargs(self):
        print('vao')
        kwargs = super().get_form_kwargs()
        kwargs['product_id'] = self.request.products.pk
        return kwargs

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated is None:
            return render(request, 'registration/login.html')
        self.extra_context['category_form'] = CatalogForm(
                                                instance=self.get_object(),
                                                user=request.user,
                                                product=Product.objects.all()
                                            )
        return render(request, self.template_name, self.extra_context)  # {'user_form': user_form, 'profile_form': profile_form}

    # def get_object(self, *args, **kwargs):
    #     category_to_edit = get_object_or_404(Category, pk=self.kwargs['pk'])
    #     return category_to_edit

    def post(self, request, *args, **kwargs):
        # if request.POST:
        form = CatalogForm(request.POST, request.FILES, instance=self.get_object(), user=request.user)
        if form.is_valid():
            obj = form.save()
            # print(form)
            # data = form.save(commit=False)
            # data.save()
            # products = request.POST.getlist('products')
            # for product in products:
            #     if Product.objects.filter(id=product).exists():
            #         product = Product.objects.get(id=product)
            #         data.products.add(product)
            return redirect('catalog:categories')

        context = self.get_context_data(form=form)
        return self.render_to_response(context)

        # else: # form not valid - each form will contain errors in form.errors
        # return render(request, self.template_name, {
        #     # 'user_form': user_form,
        #     'product_form': ProductForm
        # })

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy("catalog:categories")
