FROM nginx:1.13

RUN mkdir -p /tmp/nginx/cache
COPY ./nginx.conf /etc/nginx/nginx.conf

CMD ["nginx", "-g", "daemon off;"]