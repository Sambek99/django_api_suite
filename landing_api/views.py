from django.shortcuts import render

# Create your views here.
# landing_api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from firebase_admin import db
from datetime import datetime

class LandingAPI(APIView):
    name = "Landing API"
    collection_name = "landing_messages"  # nombre de la colección en Firebase

    def get(self, request):
        ref = db.reference(self.collection_name)
        data = ref.get()
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        ref = db.reference(self.collection_name)
        new_data = request.data.copy()
        new_data["timestamp"] = datetime.now().isoformat()
        saved_ref = ref.push(new_data)
        return Response({"message": "Dato guardado", "id": saved_ref.key}, status=status.HTTP_201_CREATED)
