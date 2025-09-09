FROM nginx:1.19-alpine

RUN rm -rf /etc/nginx/conf.d/*
RUN rm /etc/nginx/nginx.conf

COPY mysite.conf /etc/nginx/nginx.conf

EXPOSE 80