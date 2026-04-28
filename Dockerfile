FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install flask flask_sqlalchemy flask_login flask_bcrypt

CMD ["python", "app.py"]