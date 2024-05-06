from django.db import models

class Vacaciones(models.Model):
    fecha = models.DateField()
    estado = models.CharField(max_length=1,choices=[("P","Pendiente"),("A","Aprobado")])
    user_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        respuesta = f"""{self.user_id} - {self.fecha.strftime("%Y/%m/%d")}"""
        return respuesta