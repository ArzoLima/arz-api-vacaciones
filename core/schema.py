import graphene
from graphene_django import DjangoObjectType 
from vacaciones.models import Vacaciones

class VacacionesType(DjangoObjectType):
    class Meta:
            model = Vacaciones
            fields = ("id","fecha","estado","user_id")

class VacacionesInput(graphene.InputObjectType):
    user_id = graphene.Int(required=True)
    fecha = graphene.Date(required=True)
    estado = graphene.String(required=True)

class CreateVacacionesMutation(graphene.Mutation):
    class Arguments:
        vacaciones_data = graphene.List(VacacionesInput, required=True) 

    vacaciones = graphene.List(VacacionesType)

    def mutate(self, info, vacaciones_data):
        new_vacaciones = [Vacaciones.objects.create(user_id=item.user_id, fecha=item.fecha, estado=item.estado) for item in vacaciones_data]
        return CreateVacacionesMutation(vacaciones=new_vacaciones)

class DeleteVacacionesMutation(graphene.Mutation):
    class Arguments:
          userId = graphene.Int()
    
    message = graphene.String()

    def mutate(self,info,userId):
         Vacaciones.objects.filter(user_id=userId).delete()
         return DeleteVacacionesMutation(message="Elementos eliminados")

class UpdateEstadoVacacionesMutation(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int(required=True)
        estado = graphene.String(required=True)

    success = graphene.Boolean()
    updated_count = graphene.Int()

    def mutate(self, info, user_id, nuevo_estado):
        # Actualiza todos los registros que coincidan con el user_id proporcionado
        affected_rows = Vacaciones.objects.filter(user_id=user_id).update(estado=nuevo_estado)
        # Si affected_rows es mayor que 0, entonces la actualización fue exitosa
        success = affected_rows > 0
        return UpdateEstadoVacacionesMutation(success=success, updated_count=affected_rows)


class Query(graphene.ObjectType):
    hello = graphene.String(default_value="Hello!")
    vacaciones = graphene.List(VacacionesType,userId=graphene.Int())

    def resolve_vacaciones(self,info, userId):
         lista = Vacaciones.objects.filter(user_id=userId)
         return lista
    
class Mutation(graphene.ObjectType):
    create_vacaciones = CreateVacacionesMutation.Field()
    delete_vacaciones = DeleteVacacionesMutation.Field()
    update_estado_vacaciones = UpdateEstadoVacacionesMutation.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)