FROM python:3.10

WORKDIR /opt

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade pip && pip install -r requirements.txt

COPY . /opt/app/

ENV PYTHONPATH "${PYTHONPATH}:/opt/app/src/"

# async run
CMD ["uvicorn", "app.src.main:app", "--host", "0.0.0.0", "--port", "4555"]

# sync run
#ENV FLASK_APP=main_sync.py
#CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port", "4555"]
