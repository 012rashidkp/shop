from django.urls import path
from . import views
from . import views
from .views import FileUpload,deletefile


urlpatterns = [
     
    path('products/', views.get_products, name="products"),
    path('categories/', views.get_categories, name="categories"),
    path('banners/', views.get_Banners, name="banners"),
    path('fileupload/',FileUpload.as_view(),name="upload"),
    path('getfiles/', views.get_files,name="getfiles"),
    path('catwiseproduct/',views.Catwiseproduct.as_view(),name="catwise"),
    path('deletefile/',deletefile.as_view(),name="deletefile"),
    path('updatefile/', views.fileupdate.as_view(),name="updatefile")
]


