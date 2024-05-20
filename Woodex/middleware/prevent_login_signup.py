from django.shortcuts import redirect
from django.urls import reverse

class PreventLoginSignupMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        # Danh sách các URL name của trang đăng nhập và đăng ký
        if 'access' in request.session:
        # Nếu có, lấy access token từ session
            access_token = request.session['access']
            
            restricted_paths = [reverse('login'), reverse('register')]

        # Kiểm tra nếu người dùng đã đăng nhập và đang cố gắng truy cập trang đăng nhập hoặc đăng ký
            if access_token and request.path in restricted_paths:
                return redirect('/')  # Redirect người dùng đến trang chủ
            # Nếu không có access token trong session và người dùng cố gắng truy cập trang yêu cầu đăng nhập
                i 
        # Cho phép request tiếp tục nếu không phải trường hợp trên
        else:
            login_required_paths = [reverse('info'),reverse('cart'),reverse('user_order'),reverse('place_order')]
            if request.path.startswith('/add/'):
                return redirect(reverse('login')) 
            if request.path.startswith('/remove/'):
                return redirect(reverse('login'))
            if request.path in login_required_paths:
                return redirect(reverse('login'))
        return None
