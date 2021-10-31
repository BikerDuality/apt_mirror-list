FROM debian
RUN apt update
RUN apt install locales manpages-zh -y
RUN sed -i '/^#.* zh_CN.UTF-8 /s/^#//' /etc/locale.gen
RUN locale-gen
ENV LANG='zh_CN.utf8'
RUN apt-get install --reinstall ca-certificates -y
RUN sed -i "s/http:\/\/deb.debian.org\/debian/mirror+https:\/\/raw.githubusercontent.com\/BikerDuality\/apt_mirror-list\/main\/debian\/mirrors.txt/g" /etc/apt/sources.list