# from pytube import YouTube
import youtube_dl

def get_youtube_title(video_url):
    try:
        ydl_opts = {}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=False)
            video_title = info_dict.get("title", None)
            return video_title
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Provide the YouTube link as an argument to the function
with open('youtubeLinks.txt','r') as ytList:
    counter=0
    for line in ytList:
        
        ind,youtube_link = line.strip().split()

        title = get_youtube_title(youtube_link)
        with open('new_titles.txt','a',encoding='utf-8') as new_titles:
            
            if title:
                new_titles.write(f"{ind} {title}\n")
            else:
                print(f"{youtube_link}\n")
        counter+=1
        #TODO(cdomkam) this should go to len(ytList) but only need the first 100 of elements
        if counter>=100: break
