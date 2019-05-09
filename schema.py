import graphene
import api.user.schema


class Query(
    api.user.schema.Query
):
    """Root for HairQ grahql queries"""
    pass


class Mutation(
    api.user.schema.Mutation
):
    """Root for HairQ graphql mutations"""
    pass


schema = graphene.Schema(mutation=Mutation, query=Query)
