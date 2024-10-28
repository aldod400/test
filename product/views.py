from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Product
from .serializers import ProductSerializer
from .filters import ProductFilter
from utils.general_response import success_response, error_response
from rest_framework.views import APIView

# Create your views here.

# @api_view(['GET'])
# def get_by_id(request, id):
    
#     try:
#         product = Product.objects.get(id = id)
#     except:
#         product = None
#     if not product:
#         return error_response(404, "Product Not Found", 404)
#     serializer = ProductSerializer(product)
#     return Response({"product" : serializer.data})


class ProductView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, id = None):
        if id is not None:
            try:
                product = Product.objects.get(id = id)
            except:
                product = None
            if not product:
                    return error_response(404, "Product Not Found", 404)
            serializer = ProductSerializer(product)
            return success_response(200, 'Success', {"Product": serializer.data})
        
         # get products with filter and pagination
        products = ProductFilter(request.GET, queryset=Product.objects.all().order_by('id'))
        paginator = PageNumberPagination()
        paginator.page_size = 2
        queryset = paginator.paginate_queryset(products.qs, request)
        serializer = ProductSerializer(queryset, many = True)
        return success_response(200, 'Success', {"products": serializer.data})
        
        # get products with filter
        
        # products = ProductFilter(request.GET, queryset=Product.objects.all().order_by('id'))
        # serializer = ProductSerializer(products.qs, many = True)
        # return Response({"products" : serializer.data})
        
        
        # get products without filters
        
        # products = Product.objects.all()
        # serializer = ProductSerializer(products, many = True)
        # return Response({"product" : serializer.data})
        
    def post(self, request):
        data = request.data
        serializer = ProductSerializer(data = data)
        if not serializer.is_valid():
            return error_response(400, serializer.errors, 400)
        product = Product.objects.create(**data, user = request.user)
            # name        = data['name'],
            # description = data['description'],
            # price       = data['price'],
            # brand       = data['brand'],
            # category    = data['category'],
            # rating      = data['rating'],
            # stock       = data['stock'],
            # user        = request.user
        serializer = ProductSerializer(product)
        return success_response(201, 'Success', {'Product' : serializer.data})
        
    def put(self, request, id):
        data = request.data
        
        try:
            product = Product.objects.get(id = id)
        except:
            product = None
        if not product:
            return error_response(404, "Product Not Found", 404)
        
        if product.user != request.user:
            return error_response(403, 'not Allowed', 403)
        if 'name' in data:
            product.name = request.data['name']
        if 'description' in data:
            product.description = request.data['description']
        if 'price' in data:
            product.price = request.data['price']
        if 'brand' in data:
            product.brand = request.data['brand']
        if 'category' in data:
            product.category = request.data['category']
        if 'rating' in data:
            product.rating = request.data['rating']
        if 'stock' in data:
            product.stock = request.data['stock']
        product.save()
        serializer = ProductSerializer(product)
        return success_response(200, 'Updated', {'Product': serializer.data})
    
    def delete(self, request, id):
        try:
            product = Product.objects.get(id = id)
        except:
            product = None
        if not product:
            return error_response(404, "Product Not Found", 404)
        product.delete()
        return success_response(200, 'Product Delete Successfully')