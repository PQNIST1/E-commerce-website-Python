from django.urls import path
from .views import home,register,Login,Logout,product,blog,info,add_to_cart,cart,remove_from_cart,remove_to_cart,search_view,rating,place_order,user_order_details,add_comment
urlpatterns = [
     path('',home , name='home'),
    path('register/',register, name="register"),
    path('login/',Login, name="login"),
    path('logout/',Logout, name="logout"),
    path('product/<int:id>/',product, name="product"),
    path('comment/<int:id>/',add_comment, name="comment"),
    path('blog/<int:id>/',blog, name="blog"),
    path('info/',info, name="info"),
    path('add/<int:product_id>/',add_to_cart, name="add"),
    path('cart/',cart, name="cart"),
    path('remove/<int:product_id>/',remove_from_cart, name="remove"),
    path('del/<int:product_id>/',remove_to_cart, name="del"),
    path('search/', search_view, name='search'),
    path('rating/<int:product_id>/', rating, name='rating'),
    path('place_order/', place_order, name='place_order'),
    path('user_order/', user_order_details, name='user_order'),
]