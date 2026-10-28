# Self-built Reader image: upstream backend jar (byte-identical except
# web assets) + frontend built from this repo's patched source.
# Build from the repository root:
#   docker build -f deploy/Dockerfile -t jeff/reader:2.5.4-slim-patched1 .
FROM node:16-alpine AS web
WORKDIR /app/web
COPY web/ ./
RUN yarn install --ignore-engines --network-timeout 600000 --non-interactive
RUN yarn build

FROM changshengyu/reader:2.5.4-slim AS base

FROM alpine:3.21 AS patcher
RUN apk add --no-cache python3
COPY --from=base /app/bin/reader.jar /work/reader.jar
COPY --from=web /app/web/dist /work/dist
COPY deploy/patch_jar.py /work/patch_jar.py
RUN python3 /work/patch_jar.py /work/reader.jar /work/dist /work/reader-patched.jar

FROM changshengyu/reader:2.5.4-slim
COPY --from=patcher /work/reader-patched.jar /app/bin/reader.jar
