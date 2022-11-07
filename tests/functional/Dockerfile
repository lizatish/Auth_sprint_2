FROM python:3.10

WORKDIR /opt

COPY tests/functional/requirements.txt $WORKDIR/tests/functional/requirements.txt

RUN pip install --upgrade pip && pip install --no-cache-dir -r $WORKDIR/tests/functional/requirements.txt

COPY tests/ /opt/tests
COPY auth-flask-solution /opt/auth-flask-solution

ENV PYTHONPATH "${PYTHONPATH}:/opt/tests/"
ENV PYTHONPATH "${PYTHONPATH}:/opt/auth-flask-solution/src/"

