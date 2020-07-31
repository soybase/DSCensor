FROM python:3.8-alpine3.12 as dev
WORKDIR /app
ENV PYTHONPATH=/app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
USER nobody

FROM dev AS prod
COPY ./dscensor/server .
# use --preload so panparser reads clusters into memory before forking worker processes
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--preload", "dscensor:app"]
EXPOSE 8000
HEALTHCHECK CMD wget --quiet --spider http://localhost:8000/ || exit 1
