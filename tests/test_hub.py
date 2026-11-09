from html.parser import HTMLParser
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
class Links(HTMLParser):
    def __init__(self):
        super().__init__();self.links=[]
    def handle_starttag(self,tag,attrs):
        if tag=='a':
            self.links.extend(v for k,v in attrs if k=='href')

def test_local_hub_links_exist():
    for page in (ROOT/'docs').glob('*.html'):
        parser=Links();parser.feed(page.read_text())
        for link in parser.links:
            if not link.startswith(('http:','https:','#','mailto:')):
                assert (page.parent/link.split('#')[0]).exists(),(page,link)

def test_current_projects_linked():
    text=(ROOT/'README.md').read_text()
    for name in ('it-helpdesk','sales-analytics','auth-log-analyzer'):
        assert f'https://github.com/lacetears/{name}' in text
    assert 'legacy' in text.lower()
