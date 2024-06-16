from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.query import Query
from appwrite.id import ID
import os


try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass


client = Client()


(client
 # Setting API Endpoint
 .set_endpoint('https://cloud.appwrite.io/v1')
 # Setting Project ID
 .set_project(os.getenv('PROJECT_ID'))
 # Setting API Key 
 .set_key(os.getenv('API_KEY'))
 )

databases = Databases(client)

def getAttribute(db_id,collection_id):
    result = databases.list_attributes(db_id,collection_id)
    attribute=result['attributes']
    
    att_lists=[]
    
    for each_attribute in attribute :
        
        name=each_attribute["key"]
        type=each_attribute["type"]
        required=each_attribute["required"]
        default=each_attribute["default"]
     
        dics={"column_name":name,"column_type":type,"required":required,"default":default} 
        att_lists.append(dics)
        
    return att_lists

def getDocument(db_id,collection_id,query=None):
    result = databases.list_documents(db_id, collection_id,query)
    document=result['documents']
    # print(document)
    doc_list=[]
    attr_lists=getAttribute(db_id,collection_id)

    for each_document in document:
        doc_id=each_document['$id']
        dic={}
        dic['id']=doc_id
        
        for each in attr_lists:
            column_name=each["column_name"]
            value=each_document[column_name]
            dic[column_name]=value
        doc_list.append(dic)
        
    return doc_list

def addDocument(db_id,collection_id,data):
    try:
        databases.create_document(db_id,collection_id, ID.unique(), data)
        return True
    except Exception as e:
        print(e)
        return False


def deleteDocument(db_id,collection_id,document_id):
    try:
        databases.delete_document(db_id, collection_id,document_id)
        return True
    except:
        return False
    
def updateDocument(db_id,collection_id,document_id,data):
    try:
        databases.update_document(db_id, collection_id, document_id,data)
        return True
    except Exception as e:
        print("Error Editing document : ",e)
        
        return False