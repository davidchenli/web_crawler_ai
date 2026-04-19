FROM selenium/standalone-chrome:latest
USER root
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3.11-dev \
    python3.11-venv \
    python3-pip \
    --no-install-recommends \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1
RUN python3 -m ensurepip --upgrade \
    && python3 -m pip install --upgrade pip

WORKDIR /
COPY requirements.txt .
RUN python3 -m pip install --no-cache-dir -r requirements.txt --break-system-packages
COPY . .
CMD ["python3", "main.py"]