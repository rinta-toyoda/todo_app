FROM python:3.10

WORKDIR /app

COPY ./app /app

# requirements.txtから必要なライブラリをinstall
RUN pip install --no-cache-dir -r /app/requirements.txt

# uvicornでFastAPIアプリケーションを起動
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]