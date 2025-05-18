# Build-Stage
FROM node:18-slim AS build
WORKDIR /app
# package.json + yarn.lock
COPY package.json yarn.lock ./
RUN sed -i '/"fsevents"/d' package.json
RUN yarn install --frozen-lockfile
COPY . .
RUN yarn build

# Runtime-Stage mit Nginx
FROM nginx:alpine AS runtime
# Statisches Verzeichnis
WORKDIR /usr/share/nginx/html
# Eigene Nginx-Config
COPY nginx.conf /etc/nginx/nginx.conf
# Inhalte aus build kopieren
COPY --from=build /app/dist .
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]