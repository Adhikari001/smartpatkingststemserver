from jsonschema import ValidationError

from rest_framework import status
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
from rest_framework.response import Response


class Validate():
    def getValidate(self, request):
            token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
            print(token)
            data = {'token': token}
            try:
                valid_data = VerifyJSONWebTokenSerializer().validate(data)
                user = valid_data['user']
                return user
            except ValidationError :
                return Response({"Message":"Invalid JWT"}, status=status.HTTP_400_BAD_REQUEST)