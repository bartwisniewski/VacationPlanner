FROM python:3.10-alpine

WORKDIR /app

COPY ./requirements.txt .
COPY ./source/vpcoreproject/ .
COPY ./deployment/dev/scripts/ /scripts

RUN pip install --no-cache-dir -r requirements.txt \
    && sed -i 's/\r$//' /scripts/run.sh \
    && chmod -R +x /scripts

ENV PATH="/scripts::$PATH"

CMD ["/bin/bash", "-c", "run.sh"]
