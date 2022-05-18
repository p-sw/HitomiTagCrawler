import requests
from bs4 import BeautifulSoup
from datetime import datetime
import sqlite3

nowtime = datetime.now()
db = sqlite3.connect(f'Tags_[{nowtime.year}-{nowtime.month}-{nowtime.day}].db')
cursor = db.cursor()

table_cr = '''
CREATE TABLE IF NOT EXISTS Tags (
    Prefix varchar(255),
    Tag varchar(255),
    PostLength int
)
'''

cursor.execute(table_cr)
db.commit()

FEMALE = '♀'
MALE = '♂'

for alphabet_num in range(ord('a'), ord('z')+1):
    api_url = f'https://hitomi.la/alltags-{chr(alphabet_num)}.html'
    print(f'SENT GET TO {api_url}')
    response = requests.get(api_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    for posts in soup.find_all('ul', {'class': 'posts'}):
        for item in posts.find_all('li', recursive=False):
            tag = item.get_text()
            tag = tag.replace(" ", "_")
            tag_num = tag[tag.index('(')+1:tag.index(')')]
            tag = tag[:tag.index('(')]
            prefix = "tag"
            if FEMALE in tag:
                prefix = "female"
                tag = tag[:tag.index(FEMALE)]
            elif MALE in tag:
                prefix = "male"
                tag = tag[:tag.index(MALE)]
            if tag[-1] == '_':
                tag = tag[:-1]
            print(f'("{prefix}", "{tag}", {tag_num})')
            cursor.execute(f'INSERT INTO Tags VALUES ("{prefix}", "{tag}", {tag_num})')
db.commit()