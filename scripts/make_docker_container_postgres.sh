docker run -d --name pardesit14 \
    -v /Users/zundel/Documents/pardesit14 \
    -it --expose 5432 -p 5432:5432 \
    -e 'POSTGRES_PASSWORD=test123' postgres:14.19-alpine3.21
