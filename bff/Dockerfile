FROM golang:1.24

WORKDIR /app

RUN go install google.golang.org/protobuf/cmd/protoc-gen-go@v1.34.1 && \
    go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@v1.3.0 && \
    export PATH="$PATH:$(go env GOPATH)/bin"

COPY ./bff/go.mod ./bff/go.sum ./bff/
WORKDIR /app/bff
RUN go mod download

COPY ./bff /app/bff
COPY ./grpc /app/grpc

RUN chmod +x /app/bff/entrypoint.sh

CMD ["/app/bff/entrypoint.sh"]