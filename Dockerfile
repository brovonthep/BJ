FROM nginx:alpine 
LABEL org.opencontainers.image.source https://github.com/brovonthep/bj
COPY ./html /usr/share/nginx/html



### docker push ghcr.io/brovonthep/bj:latest  docker build -t ghcr.io/brovonthep/bj:latest . 
