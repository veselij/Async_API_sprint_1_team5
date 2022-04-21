from elasticsearch import AsyncElasticsearch

es: AsyncElasticsearch


async def get_elastic() -> AsyncElasticsearch:
    return es
