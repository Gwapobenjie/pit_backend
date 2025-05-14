from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework.views import APIView
from django.contrib.auth import login

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            login(request, user)
            return Response({"message": "Login successful"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# New View for Receiving Temperature Data
class TemperatureView(APIView):
    def post(self, request):
        # Get temperature data from the request body
        temp = request.data.get('temperature')
        
        if temp is not None:
            # Here you can process the temperature (e.g., store it in a database)
            print(f"Received Temperature: {temp} °C")
            
            # Return a success response
            return Response({"message": f"Temperature {temp} received successfully!"}, status=status.HTTP_200_OK)
        
        # If temperature is missing in the request
        return Response({"error": "Temperature data is missing"}, status=status.HTTP_400_BAD_REQUEST)