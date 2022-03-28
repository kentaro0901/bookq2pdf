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

    def login(self, secrets_file :str='secrets.json'):
        """Log in to BookQ.

        Args:
            secrets_file (str): Path to the json file containing your ID and password.
        """
        with open(secrets_file, 'r') as f:
            secrets = json.load(f)
        self._session = requests.session()
        login = self._session.get(f'{Bookq.URL}/login')
        soup = BeautifulSoup(login.text, 'html.parser')
        csrf = soup.select_one('input[name=_csrf]').get('value')
        login = self._session.post(f'{Bookq.URL}/login', data={'userid': secrets['id'], 'password': secrets['passwd'],'_csrf': csrf})

    def _fetch_imgs(self, book_id :str, page_num :int, sleep_seconds :float) -> list[bin]:
        """Fetch slides from BookQ as image.

        Args:
            book_id (str): ID assigned to the book(slides).
            page_num (int): Number of slides.
            sleep_seconds (float): Time interval to fetch each slide.

        Returns:
            list[bin]: List of binary data of images.
        """
        imgs = []
        for page in tqdm(range(1, page_num+1)):
            request = self._session.get(f'{Bookq.URL}/contents/unzipped/{book_id}_2/OPS/images/out_{page}.jpg', stream=True)
            if request.status_code == 200:
                imgs.append(request.content)
                time.sleep(sleep_seconds)
            else:
                break
        return imgs

    def get_pdf(self, book_url :str, page_num :int, file_name :str='output.pdf', sleep_seconds :float=1):
        """Get slides from BookQ as pdf.

        Args:
            book_url (str): URL assigned to the book(slides).
            page_num (int): Number of slides.
            file_name (str): Name of output file.
            sleep_seconds (float): Time interval to fetch each slide.
        """
        book_id = re.findall(r'contents=.+', book_url)[0].replace('contents=', '')
        imgs = self._fetch_imgs(book_id, page_num, sleep_seconds=sleep_seconds)
        with open(file_name,'wb') as f:
            f.write(img2pdf.convert(imgs))
        print(f'\"{file_name}\" is generated.')