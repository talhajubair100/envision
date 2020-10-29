from product.models import Category, Item


def mycontetxt(request):
    categories = Category.objects.all()
    return {'categories': categories}

