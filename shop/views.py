from django.shortcuts import render
from django.views import View


from .models import Product,ProductCategory,ProductImage

class IndexView(View):
    
    def get(self, request, *args, **kwargs):

        context                 = {}
        context["products"]     = Product.objects.all()


        return render(request,"shop/index.html",context)

index   = IndexView.as_view()



