FROM python:3.9-slim

WORKDIR /usr/app

# Criar diretório de logs
RUN mkdir logs

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 3333

CMD ["python", "main.py"]