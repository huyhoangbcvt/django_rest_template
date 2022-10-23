from datetime import datetime
from django.shortcuts import render, resolve_url, redirect
from django.http import HttpResponse
from rest_framework.decorators import api_view
from ..apis import category_ws


def index(request):
    # profile = request.session.get('profile')
    # print("____: "+json.dumps(profile)+profile['first_name'] )
    print('Catalog: Run debug ok')
    if request.user.is_authenticated:
        return HttpResponse('Webcome to HDWebshoft')
        # return redirect('user:home')

    return render(request, "index_catalog.html",
                  {
                      'title': "Index page",
                      # 'next':'/home/',
                      'content': "Example app page for Django.",
                      'year': datetime.now().year,
                      'design': "Hà Huy Hoàng"
                  }
                  )

