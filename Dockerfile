FROM ubuntu:19.04
MAINTAINER ArMaxRi <armaxri@gmail.com>

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

# For debugging:
RUN apt-get install nano -y

RUN pip3 install webdavclient3

COPY drone_webdav.py /bin/
RUN chmod +x /bin/drone_webdav.py

COPY scripts/webdav_copy /bin/
RUN chmod +x /bin/webdav_copy

COPY scripts/webdav_delete /bin/
RUN chmod +x /bin/webdav_delete

COPY scripts/webdav_download /bin/
RUN chmod +x /bin/webdav_download

COPY scripts/webdav_list /bin/
RUN chmod +x /bin/webdav_list

COPY scripts/webdav_mkdir /bin/
RUN chmod +x /bin/webdav_mkdir

COPY scripts/webdav_move /bin/
RUN chmod +x /bin/webdav_move

COPY scripts/webdav_upload /bin/
RUN chmod +x /bin/webdav_upload
