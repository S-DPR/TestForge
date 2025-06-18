FROM golang:1.24

WORKDIR /app

RUN apt-get update && apt-get install -y protobuf-compiler
RUN go install google.golang.org/protobuf/cmd/protoc-gen-go@v1.34.1 && \
    go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@v1.3.0

ENV PATH="$PATH:/go/bin"

COPY ./services/api-gateway /app/api-gateway
COPY ./libs/grpc /app/grpc
WORKDIR /app/api-gateway
RUN go mod download

RUN chmod +x /app/api-gateway/entrypoint.sh

CMD ["/app/api-gateway/entrypoint.sh"]