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

FROM prod AS soybase

# change to --chmod after https://github.com/moby/buildkit/pull/1492
ADD --chown=nobody:nobody \
   https://soybase.org/data/public/Glycine_sp/mixed.pan2.TV81/glysp.mixed.pan2.TV81.clust.tsv.gz \
   https://soybase.org/data/public/Glycine_sp/mixed.pan2.TV81/glysp.mixed.pan2.TV81.hsh.tsv.gz \
   panparser/
