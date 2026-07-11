# ---------- Build Stage ----------
FROM node:16 AS builder

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

RUN npm run build

# ---------- Production Stage ----------
FROM nginx:alpine

COPY --from=builder /app/build /usr/share/nginx/html

COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]



# FROM node:16

# WORKDIR /app

# COPY package.json /app/package.json
# COPY package-lock.json /app/package-lock.json

# RUN npm install

# COPY . /app
# # Create cache directory and give proper ownership
# RUN mkdir -p /app/node_modules/.cache \
#     && chown -R node:node /app

# # Run the application as the node user
# USER node

# CMD ["npm", "start"]