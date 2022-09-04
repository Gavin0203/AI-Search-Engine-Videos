import os
import time
from turtle import title
import requests
from tqdm.auto import tqdm
from bs4 import BeautifulSoup

#Listing the contents of the data dir.
video_ids = os.listdir("../data")
print(video_ids[:5])

#Listing the timestamp dirs from various video ids.
splits = sorted(os.listdir(f"../data/{video_ids[0]}"))
print(splits[:5])

#Visualizing the text transcription from the timestamps
with open(f"../data/{video_ids[0]}/{splits[0]}/subtitles.txt") as f:
    text = f.read()
print(text)

#Looping through all the files to build a dataset of video_id, text, start_second, end_second and url
dataset = []

for vid in tqdm(video_ids):
    splits = sorted(os.listdir(f"../data/{vid}"))
    vid_start = "00:00:00"
    doc = "" 
    for x,y in enumerate(splits):
        with open(f"../data/{video_ids}/{y}/subtitles.txt") as f:
            txt = f.read()
            doc += " " + txt

            #We loop untill we get 3-4 sentences.
        if len(doc) > 360:
            vid_end = s.split("-")[1].split(",")[0]
            #Extract string timestamps to actual datetime objects
            start = time.strptime(vid_start,"%H:%M:%S")
            end = time.strptime(vid_end,"%H:%M:%S") 

            #Now we convert all to seconds.
            start_sec = start.tm_sec + start.tm_min * 60 + start.tm_hour * 3600
            end_sec = end.tm_sec + end.tm_min * 60 + end.tm_hour * 3600

            #Appending all to a list
            dataset.append({
                "video_id" : vid,
                "text" : doc,
                "start_second" : start_sec,
                "end_sec" : end_sec,
                "url" : f"https://www.youtube.com/watch?v={video_ids}&t={start_sec}s"
            })
            #Update timestamp for next chunk
            vid_start = vid_end
            passage = ""

print(dataset[:3])

#Extracting metadata like video title etc using BS.
metadata = {}
for id in tqdm(video_ids):
    r = requests.get(f"https://www.youtube.com/watch?v={video_ids}")
    soup = BeautifulSoup(r.content,'lxml')
    try : 
        title = soup.find("meta", property="og:title").get("content")
        thumbnail = soup.find("meta",property="og:image").get("content")
        metadata["id"] = {"title":title,"thumbnail" : thumbnail}
    except Exception as e:
        print(e)
        print(id)
        metadata[id] = {"title" : "", "thumbnail" : ""}

print(len(metadata))

#Adding the metadata to the existing dataset
for i, doc in enumerate(dataset):
    id = doc['video_id']
    meta = metadata[id]
    #adding to existing dataset
    dataset[i] = {**doc,**meta}

#Uploading to Huggingface

