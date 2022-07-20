"""_summary_

Returns:
    _type_: _description_
"""

import re
import time
from bs4 import BeautifulSoup
import arxiv
import requests
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler



class PaperScraper:
    """
    _summary_

    """
    def __init__(
        self,
        note_path,
        paper_path='downloaded_papers/',
        download_papers=False,
        wait_time=45,
    ) -> None:
        """_summary_

        Args:
            note_path (_type_): _description_
            paper_path (str, optional): _description_. Defaults to 'downloaded_papers/'.
        """
        self.note_path = note_path
        self.paper_path = paper_path
        self.download_papers = download_papers
        self.wait_time = wait_time

    def find_url(self):
        """_summary_

        Returns:
            _type_: _description_
        """

        # url_pattern = re.compile(r"http[:\w*\./]+\d(?=\w*)")
        url_pattern = re.compile(r"http[:\w*\./.?=]+")
        file_content = [line for line in open(self.note_path)]

        writer = open(self.note_path, 'w')
        for line in file_content:
            url = url_pattern.findall(line)
            if url:
                print(f'Delaying search by {self.wait_time} seconds to avoid bot detection...')
                time.sleep(self.wait_time)
                print(url[0])
                paper_info = self.get_paper_info(url[0])
                writer.write(
                    f"* **{paper_info['title']}.**  \
                    _{paper_info['publication_info']}_ \
                    [[PDF]({paper_info['paper_dir']})] \
                    [[arxiv]({paper_info['arxiv_link']})]\
                    (Citations: **{paper_info['citation_number']}**)"
                    )
                print('Paper added!')
            else:
                writer.write(line)



    def get_paper_info(self, url):
        """_summary_

        Args:
            url (_type_): _description_

        Returns:
            _type_: _description_
        """
        id_list = re.findall(r'[0-9]+\.[0-9]+', url)
        paper = next(arxiv.Search(id_list=id_list).results())
        if self.download_papers:
            paper.download_pdf(dirpath='downloaded_papers/')


        headers = {
            'User-agent':
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5  Safari/605.1.15",
            # 'referer':'https://www.google.com/',
        }

        params = {
            "q": paper.title,
            "hl": "en",
        }

        html = requests.get(
            url='https://scholar.google.com/scholar',
            headers=headers,
            params=params).text

        soup = BeautifulSoup(html, 'lxml')
        result = soup.select('.gs_ri')[0]
        title = result.select_one('.gs_rt').text
        _cit_num = result.select_one('.gs_fl a:nth-child(3)').text
        citation_number = int(re.findall(r'\d+', _cit_num)[0])
        publication_info = result.select_one('.gs_a').text

        try:
            all_article_versions = result.select_one('a~ a+ .gs_nph')['href']
        except:
            all_article_versions = None

        data = {
            'title': title,
            'authors': " ".join([person.name for person in paper.authors]),
            'publication_info': publication_info,
            'citation_number': citation_number,
            'paper_dir': self.paper_path + paper._get_default_filename(),
            'arxiv_link': url,
        }

        return data


class Handler(FileSystemEventHandler):
    def __init__(self) -> None:
        super().__init__()

    def on_modified(self, event):
        print(f'event type: {event.event_type}  path : {event.src_path}')
        if event.src_path[-3:] == '.md':
            scraper = PaperScraper(event.src_path)
            try:
                scraper.find_url()
            except FileNotFoundError:
                print(f"Not a file: {event.src_path}")

        # if event.src_path == (os.getcwd() + '/markdown/*'):


# observer = Observer()
# observer.schedule(Handler(), path="markdown", )
# observer.start()

# try:
#     while True:
#         pass
# except KeyboardInterrupt:
#     observer.stop()

# observer.join()


if __name__ == '__main__':

    scraper = PaperScraper('markdown/nlp.md', download_papers=False)
    scraper.find_url()

    # with open(self.note_path, 'r+') as f:
    #         text = f.readlines()
    #         for line in text:
    #             regex_pattern = re.compile(r"http[:\w*\./]+\d(?=\w*)")
    #             url = regex_pattern.findall(line)
    #             if url:

    # for url in urls:
    #     paper = scraper.get_paper_info(url)
        
    print("done!")
