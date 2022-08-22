from pyexpat import model
from rest_framework import serializers
from .models import Banner,Category,ProductImage,ProductColor,ProductSize,Product,UploadFile

class BannerSerializer(serializers.ModelSerializer):
    banner_id = serializers.CharField(source='banner_id')
    banner_name = serializers.CharField(source='title')
    banner_image=serializers.ImageField(source='image')
    class Meta:
        model = Banner
        fields=('banner_id','banner_name','banner_image')
        

class CategorySerializer(serializers.ModelSerializer):
    category_id = serializers.CharField(source='category_id')
    cat_name = serializers.CharField(source='title')
    cat_image = serializers.ImageField(source='image')

    class Meta:
        model = Category
        fields =('category_id','cat_name','cat_image')
        
class prodimageserializer(serializers.ModelSerializer):
    imageID=serializers.CharField(source="image_id",read_only=True)
    prodimages=serializers.ImageField(source="images",read_only=True)
    prodName=serializers.CharField(source="name",read_only=True)
    product_id = serializers.CharField(source="product_id", read_only=True)
    
    class Meta:
        model=ProductImage
        fields = ('imageID', 'prodimages', 'prodName', 'product_id')   

class ProdColorSerializer(serializers.ModelSerializer):
    colorID=serializers.CharField(source="color_id",read_only=True)
    prodcolors = serializers.CharField(source="colors", read_only=True)
    prodName=serializers.CharField(source="name",read_only=True)
    product_id = serializers.CharField(source="product_id", read_only=True)
    class Meta:
        model=ProductColor
        fields = ("colorID", "prodcolors", "prodName", "product_id")  
        
        
class prodSizeSerializer(serializers.ModelSerializer):
    sizeID=serializers.CharField(source="size_id",read_only=True)
    prodsizes = serializers.CharField(source="sizes", read_only=True)
    prodName=serializers.CharField(source="name",read_only=True)
    product_id = serializers.CharField(source="product_id", read_only=True)
    class Meta:
        model=ProductSize
        fields = ("sizeID", "prodsizes", "prodName", "product_id")   
        

class Productserializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category')
    category_id = serializers.CharField(source='category_id')
    product_id = serializers.CharField(source='product_id')
    prodimages = prodimageserializer(source="images",many=True,read_only=True)
    prodcolors = ProdColorSerializer(source="colors",many=True,read_only=True)
    prodsizes = prodSizeSerializer(source="sizes",many=True,read_only=True,allow_null=False)
    
    class Meta:
        model = Product
        fields = ('product_id', 'title', 'image', 'marked_price', 'selling_price', 'description', 
                  'warranty', 'return_policy', 'category_name', 'category_id', 'prodimages', 'prodcolors', 'prodsizes')  
        
        
class FileSerializer(serializers.ModelSerializer):
    file_id = serializers.CharField(source='file_id',read_only=True)
    class Meta:
        model = UploadFile
        fields = ('file_id','fileName', 'fileDesc', 'myfile')  

class multipleuploadserializer(serializers.ModelSerializer):
    fileid = serializers.CharField(source='file_id',read_only=True)
    class Meta:
        model=UploadFile
        fields = ('fileid','fileName', 'fileDesc','myfile') 
          
        
                                                 
        