import requests
from bs4 import BeautifulSoup
from datetime import datetime

FEMALE = '♀'
MALE = '♂'

nowtime = datetime.now()
filename_format = f"tags [{nowtime.year}-{nowtime.month}-{nowtime.day}].txt"

# save file init
save_file = open(filename_format, "w", encoding="utf-8")

for alphabet_num in range(ord('a'), ord('z')+1):
    api_url = f'https://hitomi.la/alltags-{chr(alphabet_num)}.html'
    print(f'SENT GET TO {api_url}')
    response = requests.get(api_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    for posts in soup.find_all('ul', {'class': 'posts'}):
        for item in posts.find_all('li', recursive=False):
            tag = item.get_text()
            tag = tag.replace(" ", "_")
            tag = tag[:tag.index('(')]
            if FEMALE in tag:
                tag = "female:"+tag[:tag.index(FEMALE)]
            elif MALE in tag:
                tag = "male:"+tag[:tag.index(MALE)]
            else:
                tag = "tag:"+tag
            if tag[-1] == '_':
                tag = tag[:-1]
            # tag save
            save_file.write(tag+"\n")

save_file.close()