FROM python:3.8.13-alpine

LABEL Maintainer="sampozki"

RUN apk update && apk add gcc \
                        libc-dev libffi-dev

WORKDIR .

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY bot.py env.cfg ./

CMD ["python3.8", "bot.py"]
