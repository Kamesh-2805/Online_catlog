from django.shortcuts import render, get_object_or_404 ,redirect
from django.contrib import messages
from .models import Product
from .models import Product, Category,Order



def order_register(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        address = request.POST.get("address")
        mobile = request.POST.get("mobile")
        city = request.POST.get("city")

        Order.objects.create(
            product=product,
            name=name,
            email=email,
            address=address,
            mobile=mobile,
            city=city
        )

        messages.success(request, "🎉 Your order has been placed successfully!")
        return redirect('order_register', product_id=product.id)

    return render(request, "order_form.html", {"product": product})

def home(request):
    return render(request, "index.html")

def product(request):
    search = request.GET.get("search", "")
    category_id = request.GET.get("category", "")

    products = Product.objects.all()

    if search:
        products = products.filter(name__icontains=search)

    if category_id:
        products = products.filter(category_id=category_id)

    categories = Category.objects.all()

    return render(request, "product.html", {
        "products": products,
        "categories": categories
    })


def details(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'details.html', {'product': product})


def add_to_wishlist(request, product_id):
    wishlist = request.session.get('wishlist', [])
    if product_id not in wishlist:
        wishlist.append(product_id)
    request.session['wishlist'] = wishlist
    return redirect('wishlist')


def remove_from_wishlist(request, product_id):
    wishlist = request.session.get('wishlist', [])
    if product_id in wishlist:
        wishlist.remove(product_id)
    request.session['wishlist'] = wishlist
    return redirect('wishlist')


def wishlist(request):
    wishlist_ids = request.session.get('wishlist', [])
    wishlist_products = Product.objects.filter(id__in=wishlist_ids)
    return render(request, 'wishlist.html', {'wishlist_products': wishlist_products})


