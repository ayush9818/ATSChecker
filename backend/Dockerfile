FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

COPY requirements.txt /home/deps/requirements.txt
RUN pip install --no-cache-dir -r /home/deps/requirements.txt && rm /home/deps/requirements.txt

WORKDIR /home/backend

COPY ats_app /home/backend/ats_app

EXPOSE 8000

ENV PYTHONPATH="/home/backend:$PYTHONPATH"

CMD ["uvicorn", "ats_app.app:app", "--host", "0.0.0.0", "--port", "8000", "--timeout-keep-alive",  "300"]
