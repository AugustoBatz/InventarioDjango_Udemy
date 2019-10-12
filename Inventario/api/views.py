from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import ProductoSerializer
from Inv.models import Producto
# Create your views here.


class ProductoList(APIView):
    def get(self, request):
        prod = Producto.objects.all()
        data = ProductoSerializer(prod, many=True).data
        return Response(data)


class ProductoDetalle(APIView):
    def get(self, request, codigo):
        prod = get_object_or_404(Producto, codigo=codigo)
        data = ProductoSerializer(prod).data
        return Response(data)


@api_view(['GET', 'POST'])
def productosList(request):
    if request.method == 'GET':
        prod = Producto.objects.all()
        data = ProductoSerializer(prod, many=True).data
        return Response(data)
    if request.method == 'POST':
        serializer = ProductoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(data)


@api_view(['GET'])
def productoDetalle(request, codigo):
    if request.method == 'GET':
        prod = get_object_or_404(Producto, codigo=codigo)
        data = ProductoSerializer(prod).data
        return Response(data)
