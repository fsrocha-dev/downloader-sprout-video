
from seleniumwire import webdriver
import os
import time
import requests

urlToDownloadPlaylist = ''
payload = {}
#https://videos.sproutvideo.com/embed/a09dddb6181eeace28/ee6e6bd210112de5?signature=O2KSAKMR5a5N63YMIQQIn%2FQuY00%3D&expires=1562019803&type=hd
def getAllFilesFromPlaylist(filepath):
    final_array = []
    with open(filepath) as fp:  
        line = fp.readline()
        cnt = 1
        while line:
          
            if(line.strip().find('.ts') > -1):
                final_array.append(line.strip())
            line = fp.readline()
            cnt += 1
    return final_array
   
aswner_url =  input("Informe a URL:")
driver = webdriver.Chrome()
driver.get(aswner_url)
playButton = driver.find_element_by_css_selector('.player-big-play-button')
playButton.click()
url_complete = ''
url_720 = ''
url_key = ''
url_for_archives = ''
newURL = False

print("Aguarde...")

time.sleep(5)

for request in driver.requests:
    if request.response:
        if(request.path.find("720.m3u8") >-1):
            url_720 = request.path
        if(request.path.find("720.key") >-1):
            url_key = request.path
        if(request.path.find(".ts") >-1):
            url_for_archives = request.path
        print(request.path)
           
response = requests.get(url_720)
if(response.status_code == 200):
    with open('files/720.m3u8','wb') as  handle:
        handle.write(response.content) 
    print("720.m3u8 GERADO COM SUCESSO!!")

keyFile =  requests.get(url_key)
if(keyFile.status_code == 200):
    with open('files/720.key','wb') as  handle:
        handle.write(keyFile.content) 
    print("720.key GERADO COM SUCESSO!!")


playlist = getAllFilesFromPlaylist('files/720.m3u8')
for item in playlist:
    if(url_for_archives.find(item) > -1):
        newURL = url_for_archives.split(item)
        print("Achou")
        break

for item in playlist:
    video = requests.get(newURL[0]+item+newURL[1])
    if(video.status_code == 200):
        with open('files/'+item,'wb') as  handle:
            handle.write(video.content) 
            print("Arquivo salvo! "+ item)


os.popen("ffmpeg -allowed_extensions ALL -i "+'files/720.m3u8'+ " -c copy -bsf:a aac_adtstoasc files/OUTPUT.mp4").read()


for item in os.listdir('files/'):
    if item.endswith(".ts"):
        os.remove(os.path.join('files/', item))
    if item.endswith('.key'):
        os.remove(os.path.join('files/', item))
    if item.endswith('.m3u8'):
        os.remove(os.path.join('files/', item))
    

    





