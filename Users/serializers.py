from rest_framework import serializers
from Users.models import CustomUser

#The serializer just making the data compatible to be entered to the database and into
# format that can be utilized and saved in the database

# class UserRegistrationSerializer(serializers.ModelSerializer):
#     """
#     Currently unused in preference of the below.
#     """
#     email = serializers.EmailField(required=True)
#     first_name = serializers.CharField(required=True)
#     last_name = serializers.CharField(required=True)
#     middle_name = serializers.CharField(required=False)
#     password = serializers.CharField(min_length=8, write_only=True)

#     class Meta:
#         model = CustomUser
#         fields = ('email', 'first_name','last_name', 'middle_name','password1', 'password2')
#         extra_kwargs = {'password1': {'write_only': True}}

#     def create(self, validated_data):
#         password = validated_data.pop('password1', None)
#         # as long as the fields are the same, we can just use this
#         instance = self.Meta.model(**validated_data)
#         if password is not None:
#             instance.set_password(password)
#         instance.save()
#         return instance
