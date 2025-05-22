from dataclasses import dataclass, field
from typing import Optional, Union

from bson import ObjectId
from pymongo import UpdateOne, InsertOne, DeleteOne
from pymongo.collection import Collection
from pymongo.results import UpdateResult, BulkWriteResult, InsertOneResult, DeleteResult

from db_manager import DBManager
from utils.decorators import time_query

USE_LOWERCASE_COLLECTION = True


@dataclass
class Base:
    """Handles MongoDB operations."""
    _id: ObjectId = field(default_factory=ObjectId)

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    def __post_init__(self):
        self.db = DBManager().get_instance()

    def _get_collection_name(self) -> str:
        """
        Get the collection name for this class.
        Checks for the get_collection_name () method, otherwise derives from class name.
        """
        if hasattr(self, 'get_collection_name') and callable(getattr(self, 'get_collection_name')):
            return self.get_collection_name()

        class_name = self.__class__.__name__
        if USE_LOWERCASE_COLLECTION:
            return class_name.lower()
        return class_name

    def __get_collection(self) -> Collection:
        """Get the MongoDB collection for this class."""
        collection_name = self._get_collection_name()
        if collection_name not in self.db.list_collection_names():
            print(f"Collection '{collection_name}' does not exist - it will be created when data is inserted")
        return self.db[collection_name]

    @time_query
    def find_one(self, query: dict = None, projection: dict = None,
                 sort: list[tuple[str, int]] = None) -> Optional[dict]:
        """ Find a single document in the collection, optionally sorted. """
        query = query or {}
        collection = self.__get_collection()
        collection_name = self._get_collection_name()
        result = collection.find_one(filter=query, projection=projection, sort=sort)

        if result:
            print(f"Found document in '{collection_name}' matching {query}" + (f" sorted by {sort}" if sort else ""))
        else:
            print(f"No document found in '{collection_name}' matching {query}" + (f" sorted by {sort}" if sort else ""))

        return result

    @time_query
    def find_many(self, query: dict = None, projection: dict | list = None,
                  sort: list = None, limit: int = 0, skip: int = 0) -> list[dict]:
        query = query or {}
        collection = self.__get_collection()
        collection_name = self._get_collection_name()
        if isinstance(projection, list):
            projection = {field: 1 for field in projection}

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
    def count_documents(self, query: dict = None) -> int:
        query = query or {}
        collection = self.__get_collection()
        collection_name = self._get_collection_name()
        count = collection.count_documents(query)
        print(f"Counted {count} documents in '{collection_name}' matching query")
        return count

    @time_query
    def update_one(self, query: dict, update: dict, upsert: bool = False) -> UpdateResult:
        collection = self.__get_collection()
        collection_name = self._get_collection_name()
        result = collection.update_one(query, update, upsert=upsert)

        if result.modified_count:
            print(f"Updated {result.modified_count} document in '{collection_name}'")
        elif result.upserted_id:
            print(f"Inserted new document in '{collection_name}' with id {result.upserted_id}")
        else:
            print(f"No documents updated in '{collection_name}' (matched: {result.matched_count})")

        return result

    @time_query
    def update_many(self, query: dict, update: dict, upsert: bool = False) -> UpdateResult:
        collection = self.__get_collection()
        collection_name = self._get_collection_name()
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
            operations: list[Union[UpdateOne, InsertOne, DeleteOne]],
            ordered: bool = True
    ) -> BulkWriteResult | None:
        if not operations:
            print("No operations provided for bulk update")
            return None

        collection = self.__get_collection()
        collection_name = self._get_collection_name()
        result = collection.bulk_write(operations, ordered=ordered)

        print(
            f"Bulk operation completed on '{collection_name}': {result.inserted_count} inserted, "
            f"{result.modified_count} modified, {result.deleted_count} deleted"
        )

        return result

    @time_query
    def insert_one(self, document: dict) -> InsertOneResult:
        collection = self.__get_collection()
        collection_name = self._get_collection_name()
        result = collection.insert_one(document)

        print(f"Inserted document into '{collection_name}' with ID: {result.inserted_id}")
        return result

    @time_query
    def insert_many(self, documents: list[dict]) -> list:
        if not documents:
            print("No documents provided for insert_many")
            return []

        collection = self.__get_collection()
        collection_name = self._get_collection_name()
        result = collection.insert_many(documents)

        print(f"Inserted {len(result.inserted_ids)} documents into '{collection_name}'")
        return result.inserted_ids

    @time_query
    def delete_one(self, query: dict) -> DeleteResult:
        collection = self.__get_collection()
        collection_name = self._get_collection_name()
        result = collection.delete_one(query)

        if result.deleted_count:
            print(f"Deleted {result.deleted_count} document from '{collection_name}'")
        else:
            print(f"No documents deleted from '{collection_name}'")

        return result

    @time_query
    def delete_many(self, query: dict) -> DeleteResult:
        collection = self.__get_collection()
        collection_name = self._get_collection_name()
        result = collection.delete_many(query)

        if result.deleted_count:
            print(f"Deleted {result.deleted_count} documents from '{collection_name}'")
        else:
            print(f"No documents deleted from '{collection_name}'")

        return result

    @time_query
    def aggregate(self, pipeline: list[dict], **kwargs) -> list[dict]:
        if not pipeline:
            print("No pipeline provided for aggregation")
            return []

        collection = self.__get_collection()
        collection_name = self._get_collection_name()
        results = list(collection.aggregate(pipeline, **kwargs))

        print(f"Aggregation completed on '{collection_name}' with {len(results)} results")
        return results

    @time_query
    def distinct(self, key: str, query: dict = None) -> list:
        query = query or {}
        collection = self.__get_collection()
        collection_name = self._get_collection_name()
        results = collection.distinct(key, query)
        print(f"Found {len(results)} distinct values for '{key}' in '{collection_name}'")
        return results

    @time_query
    def save(self):
        """
        Save this object to the database.
        Uses insert_one if the object doesn't have an _id, otherwise uses update_one.
        """
        collection = self.__get_collection()
        collection_name = self._get_collection_name()

        # Convert dataclass to dict, excluding the db attribute
        document = {k: v for k, v in self.__dict__.items() if k != 'db'}

        # Check if this document already has an _id
        if '_id' in document and document['_id'] is not None:
            # Update existing document
            result = collection.update_one({'_id': document['_id']}, {'$set': document}, upsert=True)
            if result.modified_count:
                print(f"Updated document in '{collection_name}' with ID: {document['_id']}")
            else:
                print(f"No changes to document in '{collection_name}' with ID: {document['_id']}")
            return result
        else:
            # Insert new document
            result = collection.insert_one(document)
            print(f"Inserted document into '{collection_name}' with ID: {result.inserted_id}")
            # Update the _id attribute of this object
            self.id = result.inserted_id
            return result

    def close(self):
        if hasattr(self, 'client') and self.client:
            self.client.close()
            print("MongoDB connection closed")
