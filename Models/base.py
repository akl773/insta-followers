import time
from dataclasses import dataclass, field, asdict, fields
from typing import Optional, Union, Any, ClassVar, Type, TypeVar

from bson import ObjectId
from pymongo import UpdateOne, InsertOne, DeleteOne
from pymongo.collection import Collection
from pymongo.results import UpdateResult, BulkWriteResult, InsertOneResult, DeleteResult

from db_manager import DBManager
from utils.decorators import time_query

USE_LOWERCASE_COLLECTION = True

T = TypeVar('T', bound='Base')  # For proper typing of class methods


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

    @property
    def db(self):
        return DBManager().get_instance()

    def _get_collection_name(self) -> str:
        """
        Get the collection name for this class.
        Checks for the get_collection_name() method, otherwise derives from class name.
        """
        if hasattr(self, 'get_collection_name') and callable(getattr(self, 'get_collection_name')):
            return self.get_collection_name()

        class_name = self.__class__.__name__
        if USE_LOWERCASE_COLLECTION:
            return class_name.lower()
        return class_name

    @classmethod
    def _get_collection_name_cls(cls) -> str:
        """
        Class method version of _get_collection_name.
        """
        # Check for get_collection_name as a class method
        if hasattr(cls, 'get_collection_name') and callable(getattr(cls, 'get_collection_name')):

            if not isinstance(cls.get_collection_name, classmethod):
                return cls()._get_collection_name()
            return cls.get_collection_name()

        class_name = cls.__name__
        if USE_LOWERCASE_COLLECTION:
            return class_name.lower()
        return class_name

    def __get_collection(self) -> Collection:
        """Get the MongoDB collection for this class."""
        collection_name = self._get_collection_name()
        if collection_name not in self.db.list_collection_names():
            print(f"Collection '{collection_name}' does not exist - it will be created when data is inserted")
        return self.db[collection_name]

    @classmethod
    def __get_collection_cls(cls) -> Collection:
        """Class method version of __get_collection."""
        db = DBManager().get_instance()
        collection_name = cls._get_collection_name_cls()
        if collection_name not in db.list_collection_names():
            print(f"Collection '{collection_name}' does not exist - it will be created when data is inserted")
        return db[collection_name]

    @classmethod
    @time_query
    def find_one(cls: Type[T], query: dict = None, projection: dict = None,
                 sort: list[tuple[str, int]] = None) -> Optional[dict]:
        """ Find a single document in the collection, optionally sorted. """
        query = query or {}
        collection = cls.__get_collection_cls()
        collection_name = cls._get_collection_name_cls()
        result = collection.find_one(filter=query, projection=projection, sort=sort)

        if result:
            print(f"Found document in '{collection_name}' matching {query}" + (f" sorted by {sort}" if sort else ""))
        else:
            print(f"No document found in '{collection_name}' matching {query}" + (f" sorted by {sort}" if sort else ""))

        return result

    @classmethod
    @time_query
    def find_many(cls: Type[T], query: dict = None, projection: dict | list = None,
                  sort: list = None, limit: int = 0, skip: int = 0) -> list[dict]:
        query = query or {}
        collection = cls.__get_collection_cls()
        collection_name = cls._get_collection_name_cls()
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

    @classmethod
    @time_query
    def count_documents(cls, query: dict = None) -> int:
        query = query or {}
        collection = cls.__get_collection_cls()
        collection_name = cls._get_collection_name_cls()
        count = collection.count_documents(query)
        print(f"Counted {count} documents in '{collection_name}' matching query")
        return count

    @classmethod
    @time_query
    def update_one(cls, query: dict, update: dict, upsert: bool = False) -> UpdateResult:
        collection = cls.__get_collection_cls()
        collection_name = cls._get_collection_name_cls()
        result = collection.update_one(query, update, upsert=upsert)

        if result.modified_count:
            print(f"Updated {result.modified_count} document in '{collection_name}'")
        elif result.upserted_id:
            print(f"Inserted new document in '{collection_name}' with id {result.upserted_id}")
        else:
            print(f"No documents updated in '{collection_name}' (matched: {result.matched_count})")

        return result

    @staticmethod
    def _get_update_fields(params: dict, update_fields: list[str] | None = None) -> dict[str, Any]:
        """
        Helper method to extract update fields from params dictionary.
        """
        if update_fields is None:
            # update all fields except meta fields
            return {k: params[k] for k in params if k not in ["_id", "c", "deleted"]}

        # update specified fields except meta fields
        return {k: params[k] for k in update_fields if k in params and k not in ["_id", "c", "deleted"]}

    @classmethod
    @time_query
    def update_many(cls, entities: list["Base"], query_fields=None, update_fields=None, upsert=True, session=None):
        """
        Update or insert multiple entities in a single bulk operation.
        """
        if not entities:
            print(f"No entities provided for bulk update in '{cls.__name__}'")
            return None

        # Default query fields is _id
        if query_fields is None:
            query_fields = ["_id"]

        # Get current timestamp as a Unix timestamp (float)
        current_time = time.time()  # Returns seconds since epoch as a float

        db_updates = []
        for entity in entities:
            # Get entity as dict
            params = entity.get_dict()

            # Create query params from specified fields
            query_params = {key: params[key] for key in query_fields if key in params}

            # Get update fields using helper method
            update_values = cls._get_update_fields(params, update_fields)

            # Add updated timestamp (Unix timestamp)
            update_values['u'] = current_time

            # Create the update operation
            db_updates.append(
                UpdateOne(
                    query_params,
                    {
                        "$set": update_values,
                        "$setOnInsert": {"c": current_time, "deleted": False}
                    },
                    upsert=upsert
                )
            )

        # Get collection
        collection = cls.__get_collection_cls()

        # Execute bulk write and print results
        result = collection.bulk_write(db_updates, ordered=False, session=session)
        print(
            f"Bulk operation completed on '{cls.__name__}': "
            f"{result.upserted_count} inserted, "
            f"{result.modified_count} modified"
        )

        return result

    @classmethod
    @time_query
    def bulk_write(
            cls,
            operations: list[Union[UpdateOne, InsertOne, DeleteOne]],
            ordered: bool = True
    ) -> BulkWriteResult | None:
        if not operations:
            print("No operations provided for bulk update")
            return None

        collection = cls.__get_collection_cls()
        collection_name = cls._get_collection_name_cls()
        result = collection.bulk_write(operations, ordered=ordered)

        print(
            f"Bulk operation completed on '{collection_name}': {result.inserted_count} inserted, "
            f"{result.modified_count} modified, {result.deleted_count} deleted"
        )

        return result

    @classmethod
    @time_query
    def insert_one(cls, document: dict) -> InsertOneResult:
        collection = cls.__get_collection_cls()
        collection_name = cls._get_collection_name_cls()
        result = collection.insert_one(document)

        print(f"Inserted document into '{collection_name}' with ID: {result.inserted_id}")
        return result

    @classmethod
    @time_query
    def insert_many(cls, documents: list[dict]) -> list:
        if not documents:
            print("No documents provided for insert_many")
            return []

        collection = cls.__get_collection_cls()
        collection_name = cls._get_collection_name_cls()
        result = collection.insert_many(documents)

        print(f"Inserted {len(result.inserted_ids)} documents into '{collection_name}'")
        return result.inserted_ids

    @classmethod
    @time_query
    def delete_one(cls, query: dict) -> DeleteResult:
        collection = cls.__get_collection_cls()
        collection_name = cls._get_collection_name_cls()
        result = collection.delete_one(query)

        if result.deleted_count:
            print(f"Deleted {result.deleted_count} document from '{collection_name}'")
        else:
            print(f"No documents deleted from '{collection_name}'")

        return result

    @classmethod
    @time_query
    def delete_many(cls, query: dict) -> DeleteResult:
        collection = cls.__get_collection_cls()
        collection_name = cls._get_collection_name_cls()
        result = collection.delete_many(query)

        if result.deleted_count:
            print(f"Deleted {result.deleted_count} documents from '{collection_name}'")
        else:
            print(f"No documents deleted from '{collection_name}'")

        return result

    @classmethod
    @time_query
    def aggregate(cls, pipeline: list[dict], **kwargs) -> list[dict]:
        if not pipeline:
            print("No pipeline provided for aggregation")
            return []

        collection = cls.__get_collection_cls()
        collection_name = cls._get_collection_name_cls()
        results = list(collection.aggregate(pipeline, **kwargs))

        print(f"Aggregation completed on '{collection_name}' with {len(results)} results")
        return results

    @classmethod
    @time_query
    def distinct(cls, key: str, query: dict = None) -> list:
        query = query or {}
        collection = cls.__get_collection_cls()
        collection_name = cls._get_collection_name_cls()
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

        document = self.get_dict()

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

    def get_dict(self) -> dict:
        full_dict = asdict(self)
        # Remove the db attribute
        if 'db' in full_dict:
            del full_dict['db']

        return full_dict

    @classmethod
    def from_dict(cls: Type[T], data: dict) -> T:
        """
        Create an instance of this class from a dictionary.
        Useful for converting database documents to model instances.
        """
        # Filter out any keys that aren't field names in the dataclass

        field_names = {f.name for f in fields(cls)}
        filtered_data = {k: v for k, v in data.items() if k in field_names}
        return cls(**filtered_data)

    def close(self):
        if hasattr(self, 'client') and self.client:
            self.client.close()
            print("MongoDB connection closed")
