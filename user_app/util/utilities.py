from ..serializers.user_serializer import MyTokenObtainPairSerializer


def generate_tokens(user):
    # Generate token using our custom TokenObtainPairSerializer
    refresh = MyTokenObtainPairSerializer.get_token(user=user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
