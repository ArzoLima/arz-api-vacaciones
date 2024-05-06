import graphene
from graphene_django import DjangoObjectType 
from vacaciones.models import Vacaciones

class VacacionesType(DjangoObjectType):
    class Meta:
            model = Vacaciones
            fields = ("Id","fecha","user_id")

class Query(graphene.ObjectType):
    hello = graphene.String(default_value="Hello!")
    vacaciones = graphene.List(VacacionesType)

    def resolve_vacaciones(sekf,info):
         return Vacaciones.objects.all()

schema = graphene.Schema(query=Query)