from amanara.services.qdrant_service import QdrantService

print("Creating Qdrant client...")

service = QdrantService()

print("Connected successfully!")

collections = service.client.get_collections()

print("Collections object:")
print(collections)

print("Collections list:")
print(collections.collections)