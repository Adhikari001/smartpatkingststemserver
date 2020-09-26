from jsonschema import ValidationError
import jwt

from django.contrib.auth.models import User
from rest_framework import status
# from rest_framework.authentication import SessionAuthentication
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

class GetUserInfo():
    @staticmethod
    def getUserInformation(token):
        try:
            userInfo = jwt.decode(token, '_xmr#rb!ivd!r!lauu&510hzaoi^=2(i^avuu##mhq%3@ucmmk', algorithms=['HS256'])
            return User.objects.get(pk = userInfo['user_id'])
        except:
            return Response({"Message": "Invalid JWT"}, status=status.HTTP_400_BAD_REQUEST)
        pass
