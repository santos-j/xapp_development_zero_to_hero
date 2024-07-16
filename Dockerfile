FROM alpine:3.11 as bldr

# Set the RMR library version
ARG rmr_version=4.8.0

RUN apk update && apk add autoconf automake build-base cmake libtool pkgconfig git sudo
RUN git clone --branch $rmr_version https://gerrit.oran-osc.org/r/ric-plt/lib/rmr \
    && cd rmr \
    && mkdir .build; cd .build \
    && cmake .. -DDEV_PKG=1; make install \
    && cmake .. -DDEV_PKG=0; make install

FROM python:3.8-alpine

COPY --from=bldr /usr/local/bin/rmr* /usr/local/bin/
COPY --from=bldr /usr/local/include/rmr /usr/local/include/rmr
COPY --from=bldr /usr/local/lib64/librmr* /usr/local/lib64/

ENV LD_LIBRARY_PATH=/usr/local/lib/:/usr/local/lib64

# sdl needs gcc
RUN apk update && apk add gcc musl-dev bash git

# RMR setup
RUN mkdir -p /opt/route/
COPY init/routes.rt /opt/route/routes.rt
ENV RMR_SEED_RT=/opt/route/routes.rt
ENV RMR_LOG_VLEVEL=4

# Use the latest Python xApp Framework
ARG frame_version=3.2.0

RUN git clone -b ${frame_version} https://github.com/o-ran-sc/ric-plt-xapp-frame-py /ric-plt-xapp-frame-py/
RUN pip install --upgrade pip && pip install certifi six python_dateutil setuptools urllib3 logger requests inotify_simple mdclogpy google-api-python-client msgpack ricsdl
RUN touch /ric-plt-xapp-frame-py/ricxappframe/entities/__init__.py && touch /ric-plt-xapp-frame-py/ricxappframe/entities/rnib/__init__.py
RUN pip install /ric-plt-xapp-frame-py/

# Install
COPY setup.py /tmp
COPY README.md /tmp
COPY LICENSE.txt /tmp/
COPY src/ /tmp/src
COPY init/ /tmp/init
RUN pip install /tmp
ENV PYTHONUNBUFFERED=1

# Set up ConfigMap
RUN mkdir -p /opt/ric/config && chmod -R 755 /opt/ric/config
COPY init/ /opt/ric/config
ENV CONFIG_FILE=/opt/ric/config/config-file.json

# For Default DB connection
ENV DBAAS_SERVICE_PORT=6379
ENV DBAAS_SERVICE_HOST=service-ricplt-dbaas-tcp.ricplt.svc.cluster.local

#Run
CMD run-hw-python.py
