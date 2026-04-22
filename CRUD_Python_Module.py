# Example Python Code to Insert a Document 

from pymongo import MongoClient 
from bson.objectid import ObjectId 

class AnimalShelter(object): 
    """ CRUD operations for Animal collection in MongoDB """ 
    def __init__(self,user="aacuser",password="Kilo_ren1453"): 
        # Initializing the MongoClient. This helps to access the MongoDB 
        # databases and collections. This is hard-wired to use the aac 
        # database, the animals collection, and the aac user. 
        # 
        # You must edit the password below for your environment. 
        # 
        # Connection Variables 
        # 
        USER = user 
        PASS = password 
        HOST = 'localhost' 
        PORT = 27017 
        DB = 'aac' 
        COL = 'animals' 
        # 
        # Initialize Connection 
        # 
        self.client = MongoClient('mongodb://%s:%s@%s:%d' % (USER,PASS,HOST,PORT)) 
        self.database = self.client['%s' % (DB)] 
        self.collection = self.database['%s' % (COL)] 
    
    # Create a method to return the next available record number for use in the create method
    def get_next_record_number(self):
        try:
            # Find the document with the maximum record_number
            max_record = self.collection.find_one(
                sort=[("record_number", -1)]   # Sort descending by record_number
            )
            
            if max_record and "record_number" in max_record:
                next_num = max_record["record_number"] + 1
            else:
                next_num = 1  # Start at 1 if collection is empty or no record_number field
                
            print(f"Next available record number: {next_num}")
            return next_num
            
        except Exception as e:
            print(f"Error getting next record number: {e}")
            return 1  # Fallback to 1 on error
    # Complete this create method to implement the C in CRUD. 
    def create(self, data):
        if data is not None:
            try:
                # If the user didn't provide a record_number, generate one
                if "record_number" not in data:
                    data["record_number"] = self.get_next_record_number()
                
                result = self.collection.insert_one(data)
                if result.acknowledged:
                    print(f"Document inserted successfully. Inserted ID: {result.inserted_id}")
                    return True
                else:
                    print("Insert was not acknowledged by MongoDB.")
                    return False
            except OperationFailure as e:
                print(f"MongoDB operation failed: {e}")
                return False
            except Exception as e:
                print(f"Unexpected error during create: {e}")
                return False
        else:
            raise Exception("Nothing to save, because data parameter is empty")

    # Create method to implement the R in CRUD.
    def read(self, query):
        try:
            if query is None:
                query = {}  # Default to all documents if no query provided

            cursor = self.collection.find(query)
            result_list = list(cursor)   # Convert cursor to list as required

            print(f"Read operation returned {len(result_list)} document(s).")
            return result_list

        except OperationFailure as e:
            print(f"MongoDB query failed: {e}")
            return []
        except Exception as e:
            print(f"Unexpected error during read: {e}")
            return []
        # Update method to implement the U in CRUD.
    def update(self, query, update_data):
        """
        Update documents in the collection.
        query: dict - key/value lookup pair to find documents
        update_data: dict - update operators (e.g. {"$set": {"key": "new_value"}})
        Returns: number of documents modified
        """
        if query is None or update_data is None:
            print("Query or update_data cannot be None")
            return 0
        
        try:
            # Use update_many for flexibility (can update multiple documents if needed)
            result = self.collection.update_many(query, update_data)
            modified_count = result.modified_count
            print(f"Update operation modified {modified_count} document(s).")
            return modified_count
        except OperationFailure as e:
            print(f"MongoDB update failed: {e}")
            return 0
        except Exception as e:
            print(f"Unexpected error during update: {e}")
            return 0

    # Delete method to implement the D in CRUD.
    def delete(self, query):
        """
        Delete documents from the collection.
        query: dict - key/value lookup pair to find documents to delete
        Returns: number of documents deleted
        """
        if query is None:
            print("Query cannot be None for delete operation")
            return 0
        
        try:
            # Use delete_many for flexibility (can delete multiple documents if needed)
            result = self.collection.delete_many(query)
            deleted_count = result.deleted_count
            print(f"Delete operation removed {deleted_count} document(s).")
            return deleted_count
        except OperationFailure as e:
            print(f"MongoDB delete failed: {e}")
            return 0
        except Exception as e:
            print(f"Unexpected error during delete: {e}")
            return 0