from django.shortcuts import render
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


# auth cho func, using LoginRequiredMixin cho class
@login_required()
def list_category(request):
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
    return render(request, 'blog/view_category.html', {'page_obj': page_obj})


class UploadImage(TemplateView, LoginRequiredMixin):
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
            return HttpResponseRedirect(reverse_lazy('catalog:view_upload_template_page', kwargs={'pk': obj.id}))

        context = self.get_context_data(form=form)
        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        user = request.user
        # print(user.username)
        pm = Product.objects.filter(user_id=user.id).order_by(F('created_at').desc(nulls_last=True))
        # from pprint import pprint;pprint(pm)
        form = CatalogForm(request.POST, request.FILES, user=user, product=pm)  # , user=request.user, product=pm
        return render(request, 'blog/upload_category.html', {'form': form})
        # return self.post(request, *args, **kwargs)


# Upload template
class UploadImageDisplay(DetailView, LoginRequiredMixin):
    model = Category
    template_name = 'blog/upload_category_display.html'
    context_object_name = 'UF'
