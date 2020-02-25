FROM nginx:1.17.4-alpine
ENV TERM xterm
RUN apk add bash nano
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
