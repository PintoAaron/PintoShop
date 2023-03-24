from djoser.serializers import UserCreateSerializer  as BaseUserCreateSerializer , UserSerializer as BaseUserSerializer
from store.models import Customer



class UserCreateSerializer(BaseUserCreateSerializer):
    
    #def save(self, **kwargs):
    #    user = super().save(**kwargs)
    #    Customer.objects.create(user = user)
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id','email','username','password','first_name','last_name']
        


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id','username','email','first_name','last_name']
        
        
        