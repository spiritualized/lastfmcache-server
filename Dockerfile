FROM bitnami/minideb:latest
RUN install_packages python3 virtualenv uwsgi uwsgi-plugin-python3
COPY lastfmcache-server/requirements.txt /

RUN 	virtualenv /venv -p python3 && \
		/venv/bin/pip install -r /requirements.txt && \
		rm /requirements.txt