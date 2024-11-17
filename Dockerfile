FROM fanboyingeneral/crawl4ai_copy

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Default port set via ENV, but can be overridden at runtime
ENV CRAWLER_ENGINE_PORT 8000

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${CRAWLER_ENGINE_PORT}"]


