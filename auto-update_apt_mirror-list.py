import requests
from html.parser import HTMLParser

debian_mirror_base_url='https://www.debian.org/mirror'
class debain_mirror_parser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.mirror_list=set()
        self.language_list=set()
    def handle_starttag(self, tag, attrs):
        if tag=='a':
            if attrs[0][0]=='href' and attrs[0][1].startswith('list.'):
                self.language_list.add(attrs[0][1])
            if attrs[0][0]=='rel' and attrs[0][1]=='nofollow':
                self.mirror_list.add(attrs[1][1])

debain_request=requests.get(debian_mirror_base_url+'/list')
debain_parser=debain_mirror_parser()
debain_parser.feed(debain_request.text)
language_index=0
while language_index<len(debain_parser.language_list):
    debain_request=requests.get(debian_mirror_base_url+'/'+list(debain_parser.language_list)[language_index])
    debain_parser.feed(debain_request.text)
    language_index+=1
with open('debian/mirrors.txt','w') as debain_mirror_file:
    for row in debain_parser.mirror_list:
        debain_mirror_file.write(row+'\n')

ubuntu_mirror_url='https://launchpad.net/ubuntu/+archivemirrors'
class ubuntu_mirror_parser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.mirror_list=set()
        self.href=''
    def handle_starttag(self, tag, attrs):
        if tag=='a':
            if attrs[0][0]=='href':
                self.href=attrs[0][1]
    def handle_data(self, data: str):
        if self.href!='':
            if self.href.startswith(data):
                self.mirror_list.add(self.href)
    def handle_endtag(self, tag: str):
        self.href=''
ubuntu_request=requests.get(ubuntu_mirror_url)
ubuntu_parser=ubuntu_mirror_parser()
ubuntu_parser.feed(ubuntu_request.text)
with open('ubuntu/mirrors.txt','w') as ubuntu_mirror_file:
    for row in ubuntu_parser.mirror_list:
        ubuntu_mirror_file.write(row+'\n')
