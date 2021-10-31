FROM ubuntu
RUN apt update
RUN apt install language-pack-zh-hans manpages-zh -y
RUN sh -c "echo 'LANG=zh_CN.utf8'>>/etc/default/locale"
RUN apt-get install --reinstall ca-certificates -y
RUN sed -i "s/http:\/\/archive.ubuntu.com\/ubuntu\//mirror+https:\/\/raw.githubusercontent.com\/BikerDuality\/apt_mirror-list\/main\/ubuntu\/mirrors.txt/g" /etc/apt/sources.list