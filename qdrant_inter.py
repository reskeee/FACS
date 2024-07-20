from qdrant_client import AsyncQdrantClient, models
import numpy as np
import asyncio

CLIENT = AsyncQdrantClient(url="http://localhost:6333")

async def main():
    await CLIENT.delete_collection("my_collection")

    await CLIENT.create_collection(
        collection_name="my_collection",
        vectors_config=models.VectorParams(size=10, distance=models.Distance.COSINE),
    )


    await CLIENT.upsert(
        collection_name="my_collection",
        points=[
                models.PointStruct(
                id=i,
                vector=np.random.rand(512).tolist(),
                )
                for i in range(50)
        ],
    )

   # res = await client.search(
   #    collection_name="my_collection",
   #    query_vector=np.random.rand(512).tolist(),  # type: ignore
   #    limit=10,
   # )

   # print(res)

async def min_distance(embedding):
    res = await CLIENT.search(
        collection_name="my_collection",
        query_vector=embedding,  # type: ignore
        limit=10,
    )

    return res

if __name__ == "__main__":
    asyncio.run(main())
