### Instalar as seguintes bibliotecas:
### pip install pandas openpyxl
### pip install --upgrade google-api-python-client

from googleapiclient.discovery import build
import os
import pandas as pd

api_key = '' ### Adicionar a chave da API
youtube = build('youtube', 'v3', developerKey=api_key)

channel_id = '' ### adicionar o channelid aqui

def get_channel_videos(channel_id):
    res = youtube.channels().list(id=channel_id, part='contentDetails').execute()
    playlist_id = res['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    
    videos = []
    next_page_token = None
    
    while True:
        res = youtube.playlistItems().list(playlistId=playlist_id, 
                                           part='snippet', 
                                           maxResults=50, 
                                           pageToken=next_page_token).execute()
        
        videos += res['items']
        next_page_token = res.get('nextPageToken')
        
        if next_page_token is None:
            break
    
    return videos

def list_videos_info(videos):
    videos_data = []
    for video in videos:
        video_id = video['snippet']['resourceId']['videoId']
        video_details = youtube.videos().list(id=video_id, part='snippet,statistics').execute()
        
        for detail in video_details['items']:
            title = detail['snippet']['title']
            publish_date = detail['snippet']['publishedAt']
            view_count = detail['statistics']['viewCount']
            likes = detail['statistics'].get('likeCount', 'N/A')
            
            videos_data.append([title, publish_date, view_count, likes])
    
    return videos_data

videos = get_channel_videos(channel_id)
videos_info = list_videos_info(videos)

# aqui eu crio um DataFrame com os dados
df = pd.DataFrame(videos_info, columns=['Título', 'Data de Publicação', 'Visualizações', 'Likes'])

# Exportando para o Excel
excel_file_path = 'videos_info.xlsx'
df.to_excel(excel_file_path, index=False)

print(f'Os dados foram exportados com sucesso para {excel_file_path}')