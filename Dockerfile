FROM python:slim

RUN apt-get update && apt-get install -y --no-install-recommends fontconfig

WORKDIR /srv

COPY brother_ql_web brother_ql_web
COPY pyproject.toml pyproject.toml
COPY README.md README.md
COPY setup.py setup.py
COPY config.example.json config.json

RUN pip install .

EXPOSE 8013

CMD python -m brother_ql_web --configuration /srv/config.json file:///dev/usb/lp0
