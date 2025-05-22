from dataclasses import dataclass
from typing import Optional, Union

from pymongo import UpdateOne, InsertOne, DeleteOne
from pymongo.collection import Collection
from pymongo.results import UpdateResult, BulkWriteResult, InsertOneResult, DeleteResult

from db_manager import DBManager
from utils.decorators import time_query


@dataclass
class Base:
    """Handles MongoDB operations."""

    def __init__(self):
        self.db = DBManager().get_instance()

    def __get_collection(self, collection_name: str) -> Collection:
        """Get a MongoDB collection by name."""
        if collection_name not in self.db.list_collection_names():
            print(f"Collection '{collection_name}' does not exist - it will be created when data is inserted")
        return self.db[collection_name]

    @time_query
    def find_one(self, collection_name: str, query: dict = None, projection: dict = None,
                 sort: list[tuple[str, int]] = None) -> Optional[dict]:
        """ Find a single document in the collection, optionally sorted. """
        query = query or {}
        collection = self.__get_collection(collection_name)
        result = collection.find_one(filter=query, projection=projection, sort=sort)

        if result:
            print(f"Found document in '{collection_name}' matching {query}" + (f" sorted by {sort}" if sort else ""))
        else:
            print(f"No document found in '{collection_name}' matching {query}" + (f" sorted by {sort}" if sort else ""))

        return result

    @time_query
    def find_many(self, collection_name: str, query: dict = None, projection: dict = None,
                  sort: list = None, limit: int = 0, skip: int = 0) -> list[dict]:
        query = query or {}
        collection = self.__get_collection(collection_name)
        cursor = collection.find(query, projection)

        if sort:
            cursor = cursor.sort(sort)
        if skip:
            cursor = cursor.skip(skip)
        if limit:
            cursor = cursor.limit(limit)

        results = list(cursor)
        print(f"Found {len(results)} documents in '{collection_name}' matching query")
        return results

    @time_query
    def find_with_batch(self, collection_name: str, query: dict = None, projection: dict = None,
                        batch_size: int = 100, callback=None) -> int:
        query = query or {}
        collection = self.__get_collection(collection_name)

        total_count = collection.count_documents(query)
        print(f"Processing {total_count} documents from '{collection_name}' in batches of {batch_size}")

        cursor = collection.find(query, projection).batch_size(batch_size)
        count = 0
        batch = []

        for doc in cursor:
            batch.append(doc)
            count += 1

            if len(batch) >= batch_size:
                if callback:
                    callback(batch)
                batch = []
                print(f"Processed {count}/{total_count} documents")

        if batch and callback:
            callback(batch)

        print(f"Completed processing {count} documents")
        return count

    @time_query
    def count_documents(self, collection_name: str, query: dict = None) -> int:
        query = query or {}
        collection = self.__get_collection(collection_name)
        count = collection.count_documents(query)
        print(f"Counted {count} documents in '{collection_name}' matching query")
        return count

    @time_query
    def update_one(self, collection_name: str, query: dict, update: dict, upsert: bool = False) -> UpdateResult:
        collection = self.__get_collection(collection_name)
        result = collection.update_one(query, update, upsert=upsert)

        if result.modified_count:
            print(f"Updated {result.modified_count} document in '{collection_name}'")
        elif result.upserted_id:
            print(f"Inserted new document in '{collection_name}' with id {result.upserted_id}")
        else:
            print(f"No documents updated in '{collection_name}' (matched: {result.matched_count})")

        return result

    @time_query
    def update_many(self, collection_name: str, query: dict, update: dict, upsert: bool = False) -> UpdateResult:
        collection = self.__get_collection(collection_name)
        result = collection.update_many(query, update, upsert=upsert)

        if result.modified_count:
            print(f"Updated {result.modified_count} documents in '{collection_name}'")
        elif result.upserted_id:
            print(f"Inserted new document in '{collection_name}' with id {result.upserted_id}")
        else:
            print(f"No documents updated in '{collection_name}' (matched: {result.matched_count})")

        return result

    @time_query
    def bulk_write(
            self,
            collection_name: str,
            operations: list[Union[UpdateOne, InsertOne, DeleteOne]],
            ordered: bool = True
    ) -> BulkWriteResult | None:
        if not operations:
            print("No operations provided for bulk update")
            return None

        collection = self.__get_collection(collection_name)
        result = collection.bulk_write(operations, ordered=ordered)

        print(
            f"Bulk operation completed: {result.inserted_count} inserted, "
            f"{result.modified_count} modified, {result.deleted_count} deleted"
        )

        return result

    @time_query
    def insert_one(self, collection_name: str, document: dict) -> InsertOneResult:
        collection = self.__get_collection(collection_name)
        result = collection.insert_one(document)

        print(f"Inserted document into '{collection_name}' with ID: {result.inserted_id}")
        return result

    @time_query
    def insert_many(self, collection_name: str, documents: list[dict]) -> list:
        if not documents:
            print("No documents provided for insert_many")
            return []

        collection = self.__get_collection(collection_name)
        result = collection.insert_many(documents)

        print(f"Inserted {len(result.inserted_ids)} documents into '{collection_name}'")
        return result.inserted_ids

    @time_query
    def delete_one(self, collection_name: str, query: dict) -> DeleteResult:
        collection = self.__get_collection(collection_name)
        result = collection.delete_one(query)

        if result.deleted_count:
            print(f"Deleted {result.deleted_count} document from '{collection_name}'")
        else:
            print(f"No documents deleted from '{collection_name}'")

        return result

    @time_query
    def delete_many(self, collection_name: str, query: dict) -> DeleteResult:
        collection = self.__get_collection(collection_name)
        result = collection.delete_many(query)

        if result.deleted_count:
            print(f"Deleted {result.deleted_count} documents from '{collection_name}'")
        else:
            print(f"No documents deleted from '{collection_name}'")

        return result

    @time_query
    def aggregate(self, collection_name: str, pipeline: list[dict], **kwargs) -> list[dict]:
        if not pipeline:
            print("No pipeline provided for aggregation")
            return []

        collection = self.__get_collection(collection_name)
        results = list(collection.aggregate(pipeline, **kwargs))

        print(f"Aggregation completed on '{collection_name}' with {len(results)} results")
        return results

    @time_query
    def distinct(self, collection_name: str, key: str, query: dict = None) -> list:
        query = query or {}
        collection = self.__get_collection(collection_name)
        results = collection.distinct(key, query)
        return results

    def close(self):
        if hasattr(self, 'client') and self.client:
            self.client.close()
            print("MongoDB connection closed")
