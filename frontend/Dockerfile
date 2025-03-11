# Stage 1: Build Stage
FROM node:18-alpine AS builder

WORKDIR /app

RUN npm install

COPY . .

RUN npm run build

RUN chmod +x runtime-env.sh
RUN chmod +x entrypoint.sh

# Stage 2: Production Stage
FROM node:18-alpine AS runner

WORKDIR /app

RUN npm install --production

COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/package.json ./package.json
COPY --from=builder /app/runtime-env.sh ./
COPY --from=builder /app/entrypoint.sh ./
COPY --from=builder /app/server.js ./

RUN mkdir ./SSL

EXPOSE 3000

ENTRYPOINT ["/app/entrypoint.sh"]
