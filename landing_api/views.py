from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from firebase_admin import db
from datetime import datetime

class LandingAPI(APIView):
    name = "Landing API"
    collection_name = "landing_messages"  # o como se llame tu colección

    def get(self, request):
        producto_id = request.query_params.get('productoID', None)
        ref = db.reference(self.collection_name)
        data = ref.get()

        if producto_id:
            # Buscar coincidencias por productoID
            resultados = {
                key: value for key, value in data.items()
                if value.get("productoID") == producto_id
            }

            if resultados:
                return Response(resultados, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Producto no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        ref = db.reference(self.collection_name)
        new_data = request.data.copy()
        new_data["timestamp"] = datetime.now().isoformat()
        saved_ref = ref.push(new_data)
        return Response({"message": "Dato guardado", "id": saved_ref.key}, status=status.HTTP_201_CREATED)
