"""_summary_

# TODO: cannot process more than one urls.


Returns:
    _type_: _description_
"""

import re
import time
from bs4 import BeautifulSoup
import arxiv
import requests
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


class PaperScraper:
    """
    _summary_

    """
    def __init__(
        self,
        note_path,
        paper_path='downloaded_papers/',
        download_papers=False,
        wait_time=5,
    ) -> None:
        """_summary_

        Args:
            note_path (_type_): _description_
            paper_path (str, optional): _description_.
            Defaults to 'downloaded_papers/'.
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
        url_pattern = re.compile(r"(?<!\[\[\barxiv\b\]\()http[:\w*\./.?=-]+")
        file_content = [line for line in open(self.note_path)]

        for i, line in enumerate(file_content):
            url = url_pattern.findall(line)
            if url:
                print(f"Found url in {self.note_path[-10:]}: \n {url[0]}.")
                print(f"Delaying search by {self.wait_time} seconds" +
                      "to avoid bot detection...")

                time.sleep(self.wait_time)
                try:
                    paper_info = self.get_paper_info(url[0])
                    #
                    file_content[i] = f"* **{paper_info['title']}.**" + \
                        f"  _{paper_info['publication_info']}_" + \
                        f"  [[PDF]({paper_info['paper_dir']})]" + \
                        f" [[arxiv]({paper_info['arxiv_link']})]" + \
                        f" (Citations: **{paper_info['citation_number']}**)"
                except IndexError as exception:
                    print(paper_info)
                    print(exception)

        with open(self.note_path, 'w') as file:
            for line in file_content:
                file.write(line)


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
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" +
            "(KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
            'referer': 'https://www.google.com/',
        }

        params = {
            "q": paper.title,
            "hl": "en",
            "timeout": (5, 25),
        }

        html = requests.get(
            url='https://scholar.google.com/scholar',
            headers=headers,
            params=params).text

        soup = BeautifulSoup(html, 'lxml')
        result = soup.select('.gs_ri')[0]
        title = result.select_one('.gs_rt').text
        _cit_num = re.findall(r'\d+', result.select_one('.gs_fl a:nth-child(3)').text)
        citation_number = int(_cit_num[0]) if _cit_num else 0
        publication_info = result.select_one('.gs_a').text

        # try:
        #     all_article_versions = result.select_one('a~ a+ .gs_nph')['href']
        # except Exception:
        #     all_article_versions = None

        data = {
            'title': title,
            'authors': " ".join([person.name for person in paper.authors]),
            'publication_info': publication_info,
            'citation_number': citation_number,
            'paper_dir': self.paper_path + paper._get_default_filename(),
            'arxiv_link': url,
        }

        return data


class Handler(PatternMatchingEventHandler):
    """_summary_

    Args:
        PatternMatchingEventHandler (_type_): _description_
    """

    file_cache = {}

    def __init__(
        self,
        patterns=None,
        ignore_patterns=None,
        ignore_directories=False,
        case_sensitive=False,
        download_paper=False,
    ):
        super().__init__(patterns, ignore_patterns, ignore_directories, case_sensitive)
        self.download_paper = download_paper
        print(f"[INFO] Download paper true/false: {self.download_paper}")

    def on_created(self, event):
        print(f"[CREATION]: {event.src_path[-10:]} has been created!")

    def on_moved(self, event):
        print(f"[MOVE]: Someone moved {event.src_path[-10:]} to {event.dest_path[-10:]}")

    def on_modified(self, event):
        print(f"[MODIFICATION]: {event.src_path[-10:]} has been modified!")

        seconds = int(time.time())
        key = (seconds, event.src_path)
        if key in self.file_cache:
            return
        scraper = PaperScraper(
            event.src_path,
            download_papers=self.download_paper
        )
        try:
            scraper.find_url()
        except FileNotFoundError:
            print(f"Not a file: {event.src_path}")
        self.file_cache[key] = True


if __name__ == '__main__':

    # scraper = PaperScraper('markdown/reinforcement_learning.md', download_papers=True, wait_time=5)
    # scraper.find_url()
    # print("done!")

    PATTERN = ["*.md"]
    IGNORE_PATTERNS = None
    IGNORE_DIRECTORIES = False
    CASE_SENSITIVE = True

    my_event_handler = Handler(
        PATTERN,
        IGNORE_PATTERNS,
        IGNORE_DIRECTORIES,
        CASE_SENSITIVE,
        download_paper=True
    )

    observer = Observer()
    observer.schedule(my_event_handler, path="markdown/")

    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
