FROM python:3.11-slim

WORKDIR /app


# Installing CPU version of torch to minimize size
RUN pip install --no-cache-dir torch==2.0.1+cpu -f https://download.pytorch.org/whl/torch_stable.html
RUN pip install --no-cache-dir sentence-transformers==3.2.0
RUN pip install --upgrade setuptools wheel
RUN pip install python-dotenv

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . .

EXPOSE 8000

# Set the default command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
