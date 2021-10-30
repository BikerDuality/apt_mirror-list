FROM python
RUN apt update
RUN apt install locales manpages-zh -y
RUN sed -i '/^#.* zh_CN.UTF-8 /s/^#//' /etc/locale.gen
RUN locale-gen
ENV LANG='zh_CN.utf8'
RUN pip install requests