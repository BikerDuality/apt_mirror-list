FROM python
# RUN apt update
# RUN apt install --reinstall ca-certificates -y
# RUN sed -i "s/http:\/\/deb.debian.org\/debian/mirror+https:\/\/raw.githubusercontent.com\/BikerDuality\/apt_mirror-list\/main\/debian\/mirrors.txt/g" /etc/apt/sources.list
RUN apt update &&\
    apt install locales manpages-zh -y &&\
    sed -i '/^#.* zh_CN.UTF-8 /s/^#//' /etc/locale.gen &&\
    locale-gen
ENV LANG='zh_CN.utf8'
RUN pip install requests