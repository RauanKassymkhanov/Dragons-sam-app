FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    unzip \
    curl \
    && apt-get clean

RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
    && unzip awscliv2.zip \
    && ./aws/install

RUN curl -Lo sam-installation.zip https://github.com/aws/aws-sam-cli/releases/latest/download/aws-sam-cli-linux-x86_64.zip \
    && unzip sam-installation.zip -d sam-installation \
    && ./sam-installation/install

RUN pip install --upgrade pip && pip install poetry

COPY pyproject.toml poetry.lock /app/

RUN poetry install --without dev

COPY . /app/

EXPOSE 3000

CMD ["sam", "local", "start-api", "--host", "0.0.0.0"]
