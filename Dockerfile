FROM python:3.11-slim-bullseye

WORKDIR /opt
RUN apt-get update && apt-get install -y libglu1-mesa netcat curl

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./src ./migrate.sh ./
RUN chmod +x ./migrate.sh

ENTRYPOINT ["/opt/migrate.sh"]
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--log-config", "core/logging.yaml"]