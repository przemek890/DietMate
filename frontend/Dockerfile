# Stage 1: Build Stage
FROM node:22-alpine AS builder

WORKDIR /app

COPY . .

RUN npm install
RUN npm run build

RUN chmod +x entrypoint.sh

# Stage 2: Production Stage
FROM node:22-alpine AS runner

WORKDIR /app

COPY --from=builder /app/build ./build
COPY --from=builder /app/entrypoint.sh ./entrypoint.sh
COPY --from=builder /app/package.json ./package.json
COPY --from=builder /app/node_modules ./node_modules

RUN mkdir ./SSL

EXPOSE 3000

ENTRYPOINT ["/app/entrypoint.sh"]
