FROM node:20-alpine AS builder
WORKDIR /app
COPY package.json vite.config.* ./
RUN npm install
COPY src ./src
COPY index.html ./
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
