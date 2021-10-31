import requests
from html.parser import HTMLParser
import sys
import time

if len(sys.argv)>1:
    show_log=sys.argv[1]!='--silent'
else:
    show_log=True

debian_mirror_base_url='https://www.debian.org/mirror'
class debain_mirror_parser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.mirror_list=[]
        self.language_list=[]
        self.lastlink=-1
        self.mirror_info=''
    def handle_starttag(self, tag, attrs):
        self.tag=tag
        if tag=='a':
            if attrs[0][0]=='href' and attrs[0][1].startswith('list.') and attrs[0][1] not in self.language_list:
                self.language_list.append(attrs[0][1])
            if attrs[0][0]=='rel' and attrs[0][1]=='nofollow':
                self.mirror_info=attrs[1][1]
                self.lastlink=0
    def handle_data(self, data: str):
        if self.lastlink>=0:
            if self.lastlink==2:
                self.mirror_info+='\tarch:'+' arch:'.join(data.split(' '))
            self.lastlink+=1
    def handle_endtag(self, tag: str):
        if tag=='tr':
            self.lastlink=-1
            if self.mirror_info and self.mirror_info not in self.mirror_list:
                self.mirror_list.append(self.mirror_info)
            self.mirror_info=''

debain_request=requests.get(debian_mirror_base_url+'/list')
debain_parser=debain_mirror_parser()
debain_parser.feed(debain_request.text)
language_index=0
while language_index<len(debain_parser.language_list):
    if show_log:
        print('\rdebain',language_index+1,'/',len(debain_parser.language_list),list(debain_parser.language_list)[language_index],end='')
    debain_request=requests.get(debian_mirror_base_url+'/'+list(debain_parser.language_list)[language_index])
    debain_parser.feed(debain_request.text)
    language_index+=1
with open('debian/mirrors.txt','w') as debain_mirror_file:
    print('\rdebain',len(debain_parser.language_list),'/',len(debain_parser.language_list),'done')
    debain_mirror_file.write('\n'.join(debain_parser.mirror_list))

ubuntu_mirror_base_url='https://launchpad.net'
class ubuntu_mirror_list_parser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.mirror_list=[]
        self.td_count=0
    def handle_starttag(self, tag, attrs):
        if tag=='td':
            self.td_count+=1
        if tag=='a' and self.td_count==1:
            if attrs[0][0]=='href':
                self.mirror_list.append(attrs[0][1])
    def handle_endtag(self, tag: str):
        if tag=='tr':
            self.td_count=0
class ubuntu_mirror_info_parser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.tag=''
        self.href=''
        self.value=''
        self.pre=0
        self.td_count=0
        self.architecture=''
        self.architecture_list=[]
        self.mirror_info='\t'
    def handle_starttag(self, tag, attrs):
        self.tag=tag
        if tag=='pre':
            self.pre=1
        if tag=='a' and self.pre==1:
            if attrs[0][0]=='href':
                self.href=attrs[0][1]
        if tag=='option' and attrs[0][0]=='value':
            self.value=attrs[0][1]
        if tag=='option':
            for attr in attrs:
                if attr[0]=='value':
                    self.value=attr[1]
        if tag=='td':
            self.td_count+=1
    def handle_data(self, data: str):
        if self.pre and 'deb' in data:
            if data.strip()=='deb':
                self.mirror_info+='type:deb '
            else:
                self.mirror_info+='type:deb-src '
        if self.tag=='option' and data.startswith(self.value[0].upper()+self.value[1:]):
            self.mirror_info+='codename:'+self.value+' '
        if self.tag=='td':
            if data.strip()=='\n':
                self.td_count-=1
            if self.td_count==2 and self.architecture=='':
                self.architecture=data
            if self.td_count==3 and data=='Up to date' and self.architecture not in self.architecture_list:
                self.architecture_list.append(self.architecture)
                self.mirror_info+='arch:'+self.architecture+' '
    def handle_endtag(self, tag: str):
        if tag=='pre':
            self.pre=0
        if tag=='tr':
            self.td_count=0
            self.architecture=''
def mirror_find(mirror_file_list: list,mirror_url: str):
    for info in mirror_file_list:
        if mirror_url in info:
            return info
    return ''
ubuntu_request=requests.get(ubuntu_mirror_base_url+'/ubuntu/+archivemirrors')
ubuntu_list_parser=ubuntu_mirror_list_parser()
ubuntu_list_parser.feed(ubuntu_request.text)
ubuntu_mirror_list=[]
mirror_info=''
ubuntu_refresh_all=time.localtime().tm_mday!=1
with open('ubuntu/mirrors.txt','r') as ubuntu_mirror_file:
    ubuntu_mirror_file_list=ubuntu_mirror_file.read().split('\n')
    for url in ubuntu_list_parser.mirror_list:
        if show_log:
            print('\rubuntu',len(ubuntu_mirror_list)+1,'/',len(ubuntu_list_parser.mirror_list),url,end='')
        if ubuntu_refresh_all:
            mirror_info=mirror_find(ubuntu_mirror_file_list,url[16:-8])
        if mirror_info:
            ubuntu_mirror_list.append(mirror_info)
        else:
            ubuntu_request=requests.get(ubuntu_mirror_base_url+url)
            ubuntu_info_parser=ubuntu_mirror_info_parser()
            ubuntu_info_parser.feed(ubuntu_request.text)
            ubuntu_mirror_list.append(ubuntu_info_parser.href+ubuntu_info_parser.mirror_info[:-1])
with open('ubuntu/mirrors.txt','w') as ubuntu_mirror_file:
    print('\rubuntu',len(ubuntu_list_parser.mirror_list),'/',len(ubuntu_list_parser.mirror_list),'done')
    ubuntu_mirror_file.write('\n'.join(ubuntu_mirror_list))
