import re
import time
import json

from tqdm import tqdm
import requests
from bs4 import BeautifulSoup
import img2pdf

class Bookq():
    URL = 'https://bookq.s.kyushu-u.ac.jp'
    def __init__(self):
        self._session = None
        self._imgs = []

    def login(self, secrets_file='secrets.json'):
        with open(secrets_file, 'r') as f:
            secrets = json.load(f)
        self._session = requests.session()
        login = self._session.get(f'{Bookq.URL}/login')
        soup = BeautifulSoup(login.text, 'html.parser')
        csrf = soup.select_one('input[name=_csrf]').get('value')
        login = self._session.post(f'{Bookq.URL}/login', data={'userid': secrets['id'], 'password': secrets['passwd'],'_csrf': csrf})

    def _bookq2jpg(self, book_id, page_num, sleep_time):
        for page in tqdm(range(1, page_num+1)):
            r = self._session.get(f'{Bookq.URL}/contents/unzipped/{book_id}_2/OPS/images/out_{page}.jpg', stream=True)
            if r.status_code == 200:
                self._imgs.append(r.content)
                time.sleep(sleep_time)
            else:
                break
        return

    def _jpg2pdf(self, file_name):
        with open(file_name,'wb') as f:
            f.write(img2pdf.convert(self._imgs))
        self._imgs.clear()

    def get_pdf(self, book_url, page_num, file_name='output.pdf', sleep_time=1):
        book_id = re.findall(r'contents=.+', book_url)[0].replace('contents=', '')
        try:
            self._bookq2jpg(book_id, page_num, sleep_time=sleep_time)
            self._jpg2pdf(file_name)
        except Exception as e:
            print(f'\n{e}')
        else:
            print(f'\n\"{file_name}\" is generated.')