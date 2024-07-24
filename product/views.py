from django.shortcuts import render, get_object_or_404

from product.models import Product


def product_list(request):
    product = Product.objects.all()
    context = {'product': product}
    return render(request, 'product_list.html', context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {'product': product}
    return render(request, 'product_detail.html', context)
