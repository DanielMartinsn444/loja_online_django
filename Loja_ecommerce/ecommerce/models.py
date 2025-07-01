from django.db import models
from django.contrib.auth.models import User
class Perfil(models.Model):
    usuario= models.OneToOneField(User, on_delete=models.CASCADE)
    age= models.IntegerField(
        null= True,
        blank= True
    )
    def __str__(self):
        return f"Perfil de {self.usuario.username}"
    
    