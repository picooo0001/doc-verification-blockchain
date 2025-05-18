# Kontext: Projekt-Root, liegt in backend/
FROM python:3.11-slim
WORKDIR /app

# Systemtools
RUN apt-get update \
 && apt-get install -y --no-install-recommends build-essential \
 && rm -rf /var/lib/apt/lists/*

# Python-Umgebung
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1

# Dependencies
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# App-Code
COPY backend/app ./app
COPY backend/run.py ./run.py

# Smart-Contract-Artefakte
RUN mkdir -p /contracts/artifacts/contracts/Notary.sol
COPY contracts/artifacts/contracts/Notary.sol/Notary.json /contracts/artifacts/contracts/Notary.sol/
COPY contracts/artifacts/contracts/Notary.sol/Notary.dbg.json /contracts/artifacts/contracts/Notary.sol/

EXPOSE 5001
CMD ["python", "run.py"]