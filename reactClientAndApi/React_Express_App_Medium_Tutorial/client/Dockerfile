# Usage:
#
#    Build image:
#    docker build -t angular-starter .
#
#    Run image (on localhost:8080):
#    docker run --name angular-starter -p 8080:80 angular-starter
#
#    Run image as virtual host (read more: https://github.com/jwilder/nginx-proxy):
#    docker run -e VIRTUAL_HOST=angular-starter.your-domain.com --name angular-starter angular-starter

# Stage 1, based on Node.js, to build and compile Angular

FROM node:10-alpine

WORKDIR /usr/src/app

COPY package.json package.json  
RUN npm install

COPY . .  

EXPOSE 3000
CMD ["npm", "start"]

# # Stage 2, based on Nginx, to have only the compiled app, ready for production with Nginx

# FROM nginx:1.13.9-alpine

# COPY ./config/nginx-custom.conf /etc/nginx/conf.d/default.conf
                                  
# ## Remove default nginx website
# RUN rm -rf /usr/share/nginx/html/*

# ## From ‘builder’ stage copy over the artifacts in dist folder to default nginx public folder
# COPY --from=builder /ng-app/dist /usr/share/nginx/html

# CMD ["nginx", "-g", "daemon off;"]
