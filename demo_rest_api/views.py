# demo_rest_api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import uuid

# Lista simulando base de datos en memoria
data_list = [
    {'id': str(uuid.uuid4()), 'name': 'User01', 'email': 'user01@example.com', 'is_active': True},
    {'id': str(uuid.uuid4()), 'name': 'User02', 'email': 'user02@example.com', 'is_active': True},
    {'id': str(uuid.uuid4()), 'name': 'User03', 'email': 'user03@example.com', 'is_active': False},
]

class DemoRestApi(APIView):
    def get(self, request):
        active_items = [item for item in data_list if item.get('is_active', False)]
        return Response(active_items, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        if 'name' not in data or 'email' not in data:
            return Response({'error': 'Faltan campos requeridos.'}, status=status.HTTP_400_BAD_REQUEST)

        data['id'] = str(uuid.uuid4())
        data['is_active'] = True
        data_list.append(data)
        return Response({'message': 'Dato guardado exitosamente.', 'data': data}, status=status.HTTP_201_CREATED)

class DemoRestApiItem(APIView):
    def get(self, request, item_id):
        for item in data_list:
            if item['id'] == item_id:
                return Response(item, status=status.HTTP_200_OK)
        return Response({'error': 'Elemento no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, item_id):
        new_data = request.data
        for i, item in enumerate(data_list):
            if item['id'] == item_id:
                new_data['id'] = item_id
                new_data['is_active'] = item.get('is_active', True)
                data_list[i] = new_data
                return Response({'message': 'Elemento actualizado.', 'data': new_data}, status=status.HTTP_200_OK)
        return Response({'error': 'Elemento no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, item_id):
        for item in data_list:
            if item['id'] == item_id:
                item.update(request.data)
                return Response({'message': 'Elemento actualizado parcialmente.', 'data': item}, status=status.HTTP_200_OK)
        return Response({'error': 'Elemento no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, item_id):
        for item in data_list:
            if item['id'] == item_id:
                item['is_active'] = False
                return Response({'message': 'Elemento desactivado.'}, status=status.HTTP_200_OK)
        return Response({'error': 'Elemento no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
