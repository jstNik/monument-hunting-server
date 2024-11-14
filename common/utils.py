from rest_framework import status
from rest_framework.response import Response


def extract_api_key(request):
    api_key = request.headers.get("API-KEY")
    return api_key


def client_not_authorized():
    return Response({"error": "Your client is not authorized"}, status=status.HTTP_403_FORBIDDEN)


def invalid_id():
    return Response({"error: Prompt a valid id"}, status=status.HTTP_400_BAD_REQUEST)
