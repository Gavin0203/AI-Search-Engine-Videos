#We index the data using Pinecone, we will use sentence transformer(encoding text to embeddings) and a pinecone index.
#Pinecone is vector based DB.

#Initializing sentence transformer and pinecone
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

from utils.vec_db import pinecone_init

model =   SentenceTransformer('flax-sentence-embeddings/all_datasets_v3_mpnet-base')
#Describes the model params

print(model)
#We store the model embedding to later use it in pinecone.
embedding_dimension = model.get_sentence_embedding_dimension()
index = pinecone_init(api,"us-west1-gcp",index_name="youtube-search",embedding=embedding_dimension,metric="cosine")

docs = [] #To store ids, embeddings, and metadata
batch = 64

for i in tqdm(range(0,len(ytt)),batch_size):
    i_end = min(i+batch_size , len(ytt))
    #extract batch from YT transactions data
    batch = ytt[i:i_end]
    #encode batch of text
    embeds = model.encode(batch['text']).tolist()
    #each snippet needs a unique id
    #we will merge video ID and star_seconds for this
    ids = [f"{x[0]}-{x[1]}" for x in zip(batch["video_id"],batch['start_second'])]
    #create meta records
    meta = [{
        'video_id' : x[0],
        'title' : x[1],
        'text' : x[2],
        'start_second' : x[3],
        'end_second' : x[4],
        'url' : x[5],
        'thumbnail' : x[6]
    } for x in zip(
        batch['video_id'],
        batch['title'],
        batch['text'],
        batch['start_second'],
        batch['end_second'],
        batch['url'],
        batch['thumbnail']

    )]
    #create list of (IDS,vectors,metadata) to a variable
    data = list(zip(ids,embeds,meta))
    #Add to pinecone
    index.upsert(vectors = data)

print(index.describe_index_stats)


#We now query a example, we use the same tokenizer model and pass it to Pinecone query endpoint point.
query = "What is deep learning?"

xq = model.encode([query]).tolist()

#Index querying
xc = index.query(xq, top_k = 5, include_metadata = True)

for context in xc['resuls'][0]['matches']:
    print(context['metadata']['text'],end="\n---\n")

     

