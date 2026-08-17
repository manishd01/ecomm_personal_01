# =========================================================
# DEVELOPMENT
# =========================================================

FROM node:16 AS development

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

ARG REACT_APP_API_HOST
ARG REACT_APP_ENV

ENV REACT_APP_API_HOST=$REACT_APP_API_HOST
ENV REACT_APP_ENV=$REACT_APP_ENV

EXPOSE 3000

CMD ["npm", "start"]


# =========================================================
# PRODUCTION BUILD
# =========================================================

FROM node:16 AS builder

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

ARG REACT_APP_API_HOST
ARG REACT_APP_ENV

ENV REACT_APP_API_HOST=$REACT_APP_API_HOST
ENV REACT_APP_ENV=$REACT_APP_ENV

RUN npm run build


# =========================================================
# PRODUCTION
# =========================================================

FROM nginx:alpine AS production

COPY --from=builder /app/build /usr/share/nginx/html

COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]