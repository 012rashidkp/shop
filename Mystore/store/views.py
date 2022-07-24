from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Category,Product,Banner,UploadFile
from .Serializers import BannerSerializer,CategorySerializer,Productserializer,FileSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import MultiPartParser,FormParser
from django.shortcuts import get_object_or_404




@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def get_Banners(request):
    banner = Banner.objects.all()
    serializer = BannerSerializer(
        banner, many=True, context={'request': request})
    if banner.exists():
        return Response({'error': False, 'banners': serializer.data})

    return Response({'error': True, 'message': "no datas found"})



@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def get_categories(request):
    category = Category.objects.all()
    serializer = CategorySerializer(
        category, many=True, context={'request': request})
    data = {}
    if category.exists():
        data["error"] = False
        data["categories"] = serializer.data
    else:
        data["error"] = True
        data["message"] = "no datas found"
    return Response(data)



@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def get_products(request):
    products = Product.objects.all()
    serializer = Productserializer(
        products, many=True, context={'request': request})
    data = {}
    if products.exists():
        data["error"] = False
        data["datas"] = serializer.data
    else:
        data["error"] = True
        data["message"] = "no datas found"
    return Response(data)



class ProductDetail(APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]
    def get(self, request):
        product_id = request.data.get("product_id")
        spec_prod = Product.objects.get(id=product_id)
        serializer = Productserializer(spec_prod, context={'request': request})
        data = {}
        if spec_prod != None:
            data["error"] = False
            data["datas"] = serializer.data
        else:
            data["error"] = True
            data["message"] = "no datas found"
        return Response(data)
    

class FileUpload(APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]
    parser_classes = (MultiPartParser, FormParser)
    def post(self, request, *args, **kwargs):
        file_serializer = FileSerializer(data=request.data)
        data = {}
        if file_serializer.is_valid():
            file_serializer.save()
            data["error"] = False
            data["message"] = "file uploaded successfully"
        else:
            data["error"] = True
            data["message"] = "file uploaded failed"
        return Response(data)
    
    

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def get_files(request):
    files = UploadFile.objects.all()
    filecount = UploadFile.objects.all().count()
    serializer = FileSerializer(files, many=True, context={'request': request})
    data = {}
    if files.exists():
        data["error"] = False
        data["count"] = str(filecount)
        data["files"] = serializer.data
    else:
        data["error"] = True
        data["message"] = "no datas found"
    return Response(data)


class deletefile(APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def post(self, request):
        file_id = request.data.get("file_id")
        data = {}
        if file_id is None:
            data["error"] = True
            data["message"] = "please place required parameter"
        elif file_id == "":
            data["error"] = True
            data["message"] = "file_id cannot be blank"
        idexist = UploadFile.objects.filter(id=file_id)
        if idexist:
            item = UploadFile.objects.get(id=file_id)
            item.delete()
            data["error"] = False
            data["message"] = item.fileName + "  deleted sucessfully"
        else:
            data["error"] = True
            data["message"] = f'{file_id}'+" file_id does not exist"
        return Response(data)
    

class fileupdate(APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file_id = request.data.get("file_id")
        fileDesc = request.data.get("fileDesc")
        fileName = request.data.get("fileName")
        myfile = request.data.get("myfile")
        data = {}
        if file_id or fileDesc or fileName or myfile is None:
            data["error"] = True
            data["message"] = "required parameters cannot be blank"
        if file_id == "":
            data["error"] = True
            data["message"] = "file_id cannot be blank"
        elif fileDesc == "":
            data["error"] = True
            data["message"] = "fileDesc cannot be blank"
        elif fileName == "":
            data["error"] = True
            data["message"] = "fileName cannot be blank"
        elif myfile == "":
            data["error"] = True
            data["message"] = "myfile cannot be blank"
        idexist = UploadFile.objects.filter(id=file_id)
        if idexist:
            queryset = UploadFile.objects.all()
            files = get_object_or_404(queryset, id=file_id)
            serializer = FileSerializer(
                files, data=request.data, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                data["error"] = False
                data["message"] = files.fileName + " updated sucessfully"
            else:
                data["error"] = True
                data["message"] = "something went wrong"
        return Response(data)            
    

class Catwiseproduct(APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def get(self, request):
        category_id = request.data.get("category_id")
        query = Product.objects.filter(category_id=category_id)
        serializer = Productserializer(
            query, many=True, context={'request': request})
        data = {}
        if category_id is None:
            data["error"] = True
            data["message"] = "please place required parameter"
        elif category_id == None:
            data["error"] = True
            data["message"] = "category_id cannot be blank"
        elif query.exists():
            data["error"] = False
            data["datas"] = serializer.data
        else:
            data["error"] = True
            data["message"] = "no datas found"
        return Response(data)    