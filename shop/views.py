import json
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from Woodex.helpers import custom_response
from orders.models import Order, OrderDetail
from products.models import BlogProduct, CartItem, Category, Product, ProductComment
from user.models import UserAccount
from .forms import OrderForm, RegistrationForm
import requests
from django.http import JsonResponse
from django.shortcuts import redirect,get_object_or_404
from django.urls import reverse


# Create your views here.
def get_user_profile(access_token):
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get('http://127.0.0.1:8000/api/v1/users/profile/', headers=headers)
    if response.status_code == 200:
        user_profile = response.json()
        print(user_profile)
        return user_profile
    else:
        return None

def home(request):
    products = Product.objects.all()
    categorys = Category.objects.all()
    blogs = BlogProduct.objects.all()
    if 'access' in request.session:
        # Nếu có, lấy access token từ session
        access_token = request.session['access']
        
        if access_token:
            user_profile = get_user_profile(access_token)
            if user_profile:
                user_id = user_profile['data']['id']
                cart_items = CartItem.objects.filter(user_id=user_id)
                total_quantity = 0
                for cart_item in cart_items:
                    total_quantity += cart_item.quantity
                username = user_profile['data']['username']
                # Trả về template với thông tin của người dùng nếu có
                return render(request, 'pages/home.html', {'username': username ,'products': products, 'categorys': categorys,'blogs': blogs, 'total_quantity': total_quantity})
            else:
            # Xử lý lỗi khi không thể lấy thông tin của người dùng từ token
                pass
    else:
        pass
    return render(request, 'pages/home.html', {'products': products, 'categorys': categorys,'blogs': blogs})
def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            # Xử lý lỗi nếu mật khẩu không khớp
            pass

        if UserAccount.objects.filter(username=username).exists():
            # Xử lý lỗi nếu tên người dùng đã tồn tại
            pass
        response = requests.post('http://127.0.0.1:8000/api/v1/users/', json={
            'username': username,
            'email': email,
            'password': password1
        })
        if response.status_code == 201:
            # Tạo token
            response = requests.post('http://127.0.0.1:8000/api/v1/jwt/create', data={'username': username, 'password': password1})
            if response.status_code == 200:
                token = response.json()
                # Lưu token vào session hoặc thực hiện hành động khác tùy thuộc vào yêu cầu của bạn
                request.session['access'] = token['access']
                return HttpResponseRedirect('/')
            else:
                # Xử lý lỗi khi tạo token
                pass
    return render(request, 'pages/register.html')

def Login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")

            # Tạo token bằng cách gửi yêu cầu POST tới endpoint JWT
            response = requests.post('http://127.0.0.1:8000/api/v1/jwt/create', data={'username': username, 'password': password})
            if response.status_code == 200:
                token = response.json()
                # Lưu token vào session hoặc xử lý khác tùy thuộc vào yêu cầu của bạn
                request.session['access'] = token['access']
                print(request.session['access'])
                # Redirect người dùng
                return HttpResponseRedirect("/")
            else:
                messages.error(request, "Could not create JWT token.")
        else:
            messages.error(request, "Invalid Credentials")
    return render(request, "pages/login.html")

def Logout(request):
    if 'access' in request.session:
        del request.session['access'] 
    logout(request)
    messages.success(request, "Successfully logged out")
    return HttpResponseRedirect('/login')
def product(request,id):
    product = Product.objects.get(id=id)
    if 'access' in request.session:
        # Nếu có, lấy access token từ session
        access_token = request.session['access']
        if access_token:
            user_profile = get_user_profile(access_token)
            if user_profile:
                user_id = user_profile['data']['id']
                cart_items = CartItem.objects.filter(user_id=user_id)
                total_quantity = 0
                for cart_item in cart_items:
                    total_quantity += cart_item.quantity
                username = user_profile['data']['username']
                # Trả về template với thông tin của người dùng nếu có
                return render(request, 'pages/product.html', {'username': username, "product":product,'total_quantity': total_quantity},)
            else:
            # Xử lý lỗi khi không thể lấy thông tin của người dùng từ token
                pass
    else:
        pass
    return render(request, 'pages/product.html',{"product":product})

def blog(request,id):
    blog= BlogProduct.objects.get(id=id)
    if 'access' in request.session:
        # Nếu có, lấy access token từ session
        access_token = request.session['access']
        if access_token:
            user_profile = get_user_profile(access_token)
            if user_profile:
                user_id = user_profile['data']['id']
                cart_items = CartItem.objects.filter(user_id=user_id)
                total_quantity = 0
                for cart_item in cart_items:
                    total_quantity += cart_item.quantity
                username = user_profile['data']['username']
                # Trả về template với thông tin của người dùng nếu có
                return render(request, 'pages/blog.html', {'username': username, "blog":blog,'total_quantity': total_quantity},)
            else:
            # Xử lý lỗi khi không thể lấy thông tin của người dùng từ token
                pass
    else:
        pass
    return render(request, 'pages/blog.html',{"blog":blog})
def info(request):
    if 'access' in request.session:
        # Nếu có, lấy access token từ session
        access_token = request.session['access']
        if access_token:
            user_profile = get_user_profile(access_token)
            if request.method == "POST":
                username = request.POST.get('username')
                email = request.POST.get('email')
                first_name = request.POST.get('firstname')
                last_name = request.POST.get('lastname')
                phone = request.POST.get('phone')
                address = request.POST.get('address')
                headers = {'Authorization': f'Bearer {access_token}'}
                response = requests.put('http://127.0.0.1:8000/api/v1/users/profile/', headers=headers, data={"username":username,"first_name":first_name,"last_name":last_name,"email":email,"phone":phone,"address":address})
                if response.status_code == 200:
                     return HttpResponseRedirect("info/") 
            if user_profile:
                username = user_profile['data']['username']
                user = user_profile['data']
                user_id = user_profile['data']['id']
                cart_items = CartItem.objects.filter(user_id=user_id)
                total_quantity = 0
                for cart_item in cart_items:
                    total_quantity += cart_item.quantity
                # Trả về template với thông tin của người dùng nếu có
                return render(request, 'pages/userinfo.html', {'username': username, "user":user, 'total_quantity': total_quantity},)
            else:
            # Xử lý lỗi khi không thể lấy thông tin của người dùng từ token
                pass
    else:
        pass
    return render(request, 'pages/userinfo.html',)
def add_to_cart(request, product_id):
    if request.method == "POST":
        try:
            product = Product.objects.get(id=product_id)
            data = json.loads(request.body)
            quantity = int(data.get("quantity", 0))
           
            if quantity != 0:  # Kiểm tra xem có tồn tại giá trị quantity không
                quantity = int(quantity)
            else :
                quantity = 1
            # Kiểm tra xem sản phẩm có sẵn trong kho không
            if product.amount < quantity:
                return JsonResponse({"error": "Product is out of stock."}, status=400)
            print(quantity)
            user_id = request.user
            # Kiểm tra xem sản phẩm đã tồn tại trong giỏ hàng của người dùng chưa
            cart_item, created = CartItem.objects.get_or_create(
                user_id=user_id,
                product_id=product
            )
              
            # Nếu sản phẩm đã tồn tại trong giỏ hàng, tăng số lượng theo số lượng được chỉ định
            if not created:
                cart_item.quantity += quantity
                cart_item.save()
            else:
                # Nếu sản phẩm chưa tồn tại trong giỏ hàng, thêm sản phẩm với số lượng được chỉ định
                cart_item.quantity = quantity
                cart_item.save()

            return JsonResponse({"message": "Product added to cart successfully."})

        except Product.DoesNotExist:
            return JsonResponse({"error": "Product not found."}, status=400)
def cart(request):
     if 'access' in request.session:
        # Nếu có, lấy access token từ session
        access_token = request.session['access']
        if access_token:
            user_profile = get_user_profile(access_token)
            if request.method == "POST":
                username = request.POST.get('username')
                email = request.POST.get('email')
                first_name = request.POST.get('firstname')
                last_name = request.POST.get('lastname')
                phone = request.POST.get('phone')
                address = request.POST.get('address')
                headers = {'Authorization': f'Bearer {access_token}'}
                response = requests.put('http://127.0.0.1:8000/api/v1/users/profile/', headers=headers, data={"username":username,"first_name":first_name,"last_name":last_name,"email":email,"phone":phone,"address":address})
                if response.status_code == 200:
                     return HttpResponseRedirect("info/") 
            if user_profile:
                username = user_profile['data']['username']
                user = user_profile['data']
                user_id = request.user
                cart_items = CartItem.objects.filter(user_id=user_id)
                list_item = []
                total_quantity = 0
                total_price = 0
                for cart_item in cart_items:
                    total_price += cart_item.quantity * (cart_item.product_id.price - ((cart_item.product_id.price * cart_item.product_id.discount)/100))
                for cart_item in cart_items:
                    total_quantity += cart_item.quantity
                for list_cart in cart_items:
                    list_item.append(list_cart)
                # Trả về template với thông tin của người dùng nếu có
                return render(request, 'pages/cart.html',{"list_item":list_item, "username":username, "total_quantity":total_quantity, "total_price":total_price})
            else:
            # Xử lý lỗi khi không thể lấy thông tin của người dùng từ token
                pass
def remove_from_cart(request, product_id):
    if request.method == 'POST':
        cart_item = CartItem.objects.get(product_id=product_id, user_id=request.user)
        cart_item.delete()
        return redirect('cart/')
def remove_to_cart(request, product_id):
    if request.method == "POST":
        try:
            product = Product.objects.get(id=product_id)
            data = json.loads(request.body)
            quantity = int(data.get("quantity", 0))
           
            if quantity != 0:  # Kiểm tra xem có tồn tại giá trị quantity không
                quantity = int(quantity)
            else:
                quantity = -1

            user_id = request.user
            # Kiểm tra xem sản phẩm đã tồn tại trong giỏ hàng của người dùng chưa
            cart_item, created = CartItem.objects.get_or_create(
                user_id=user_id,
                product_id=product
            )
            # Nếu sản phẩm đã tồn tại trong giỏ hàng và quantity bằng 0, xóa nó khỏi giỏ hàng
            # Nếu sản phẩm đã tồn tại trong giỏ hàng, cập nhật số lượng theo số lượng được chỉ định
            if not created:
                cart_item.quantity += quantity
                cart_item.save()
            else:
                # Nếu sản phẩm chưa tồn tại trong giỏ hàng, thêm sản phẩm với số lượng được chỉ định
                cart_item.quantity = quantity
                cart_item.save()
            if not created and cart_item.quantity == 0:
                cart_item.delete()
                return JsonResponse({"message": "Product removed from cart successfully."})
            return JsonResponse({"message": "Product added to cart successfully."})

        except Product.DoesNotExist:
            return JsonResponse({"error": "Product not found."}, status=400)
def search_view(request):
    query = request.GET.get('query', '')  # Lấy truy vấn tìm kiếm từ tham số GET

    # Thực hiện tìm kiếm sản phẩm dựa trên truy vấn
    results = Product.objects.filter(name__icontains=query)

    # Chuyển kết quả thành danh sách các đối tượng JSON
    if 'access' in request.session:
        # Nếu có, lấy access token từ session
        access_token = request.session['access']
        
        if access_token:
            user_profile = get_user_profile(access_token)
            if user_profile:
                user_id = user_profile['data']['id']
                cart_items = CartItem.objects.filter(user_id=user_id)
                total_quantity = 0
                for cart_item in cart_items:
                    total_quantity += cart_item.quantity
                username = user_profile['data']['username']
                # Trả về template với thông tin của người dùng nếu có
                return render(request, 'pages/search.html', {'username': username, 'total_quantity': total_quantity, "results":results, "username":username})
            else:
            # Xử lý lỗi khi không thể lấy thông tin của người dùng từ token
                pass
    else:
        return render(request, 'pages/search.html',{"results":results})
def rating(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request,'pages/rating.html',{"product":product})
def place_order(request):
    if request.method == 'POST':
        try:
            name = request.POST.get("receiver_name")
            phone = request.POST.get("receiver_phone")
            address = request.POST.get("receiver_address")
            note = request.POST.get("description")
            user_id = request.user
            order = Order.objects.create(
                receiver_name=name,
                receiver_phone=phone,
                receiver_address=address,
                description=note,
                user_id=user_id,  # Giả định người dùng đã được xác thực
                is_ordered=True
            )
            
            # Di chuyển sản phẩm từ Cart sang Order
            cart_items = CartItem.objects.filter(user_id=user_id)
            for item in cart_items:
                OrderDetail.objects.create(
                    order_id=order,
                    product_id=item.product_id,
                    amount=item.quantity,
                    price=item.product_id.price,
                    discount=item.product_id.discount
                )
                item.delete()  # Xóa mục trong giỏ hàng
            return redirect(reverse('user_order'))
        except Product.DoesNotExist:
            return JsonResponse({"error": "Product not found."}, status=400)
def user_order_details(request):
    # Lọc các đơn hàng của người dùng
    user_id = request.user
    user_orders = Order.objects.filter(user_id=user_id)

    # Lưu trữ tất cả chi tiết đơn hàng của người dùng
    user_order_details = []

    # Lặp qua từng đơn hàng và lấy chi tiết của mỗi đơn hàng
    for order in user_orders:
        order_details = order.order_details.all()
        user_order_details.extend(order_details)
    print(user_order_details    )
    return render(request, 'pages/order.html', {'details': user_order_details,}) 
    
def add_comment(request, product_id):
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment_text = request.POST.get('comment')
        parent_id = request.POST.get('parent_id', None)

        product = Product.objects.get(id=product_id)
        user = request.user  # Giả sử người dùng đã được xác thực

        if not user.is_authenticated:
            return HttpResponse('Unauthorized', status=401)

        if parent_id:  # Kiểm tra xem có phải là phản hồi của bình luận khác không
            parent_comment = get_object_or_404(ProductComment, pk=parent_id)
        else:
            parent_comment = None

        comment = ProductComment(
            rating=rating,
            comment=comment_text,
            product_id=product,
            user_id=user,
            parent_id=parent_comment
        )
        comment.save()

        return redirect('product', product_id=product_id)
    else:
        return HttpResponse('Invalid request', status=400)