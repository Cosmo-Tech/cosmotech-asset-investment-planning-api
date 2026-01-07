FROM python:3.13

WORKDIR src/

COPY requirements.txt .

COPY pyproject.toml .

ADD cosmotech/ cosmotech/

RUN pip install .

ENTRYPOINT [ "fastapi", "run", "cosmotech/aip/__main__.py", "--host", "0.0.0.0" , "--port", "8080"]
