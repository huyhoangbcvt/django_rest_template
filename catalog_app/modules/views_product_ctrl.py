from django.shortcuts import render, resolve_url, redirect
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
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from ..models.catalog_model import Category, Product


def list_product(request):
    # auth cho func, using LoginRequiredMixin cho class
    if not request.user.is_authenticated:
        return redirect('user:login')
    # pm = Product.objects.all()
    # sort pm = Product.objects.order_by(F('created_at').desc(nulls_last=True)) #.asc()
    # filter
    user = request.user
    print(user.username)
    # queryset
    pm = Product.objects.filter(user_id=user.id).order_by(F('created_at').desc(nulls_last=True))
    paginator = Paginator(pm, 2)  # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/view_product.html', {'page_obj':page_obj})


class UploadImage(TemplateView, LoginRequiredMixin):
    form = ProductForm
    template_name = 'blog/upload_product.html'

    def post(self, request, *args, **kwargs):
        user = request.user
        # if user is not None and user.is_superuser:
        #     user = User.objects.all()
        print(user.username)
        form = ProductForm(request.POST, request.FILES, user=request.user) #, user=request.user, product=pm
        if form.is_valid():
            obj = form.save()
            return HttpResponseRedirect(reverse_lazy('catalog:view_upload_p_template_page', kwargs={'pk': obj.id}))

        context = self.get_context_data(form=form)
        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


# Upload template
class UploadImageDisplay(DetailView, LoginRequiredMixin):
    model = Product
    template_name = 'blog/upload_product_display.html'
    context_object_name = 'UF'
