FROM nginx/unit:1.23.0-python3.9

ARG username
ARG password

COPY requirements.txt /app/
COPY ./dockerfiles/config.json /docker-entrypoint.d/config.json
RUN python -m pip install --upgrade pip
RUN pip install -r /app/requirements.txt
RUN pip install -e git+https://${username}:${password}@gitlab.com/lawchad/shared-utils.git#egg=chadutils

COPY . /app
WORKDIR /app

EXPOSE 8000
