import pinecone

def pinecone_init(api,env,index_name,embedding,metric):
    #Initializin the index
    pinecone.init(api_key = api,
              environment = index_name  )
    #Get api key from app.pinecone.io
    #create index
    pinecone.create_index("youtube-search",dimension = embedding,metrics = metric)

    #connect to new index
    index = pinecone.Index("youtube-search")
    return index