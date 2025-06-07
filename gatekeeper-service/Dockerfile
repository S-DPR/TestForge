FROM golang:1.24

WORKDIR /app

RUN apt-get update && apt-get install -y protobuf-compiler
RUN go install google.golang.org/protobuf/cmd/protoc-gen-go@v1.34.1 && \
    go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@v1.3.0

ENV PATH="$PATH:/go/bin"

COPY ./gatekeeper-service /app/gatekeeper-service
COPY ./grpc /app/grpc
WORKDIR /app/gatekeeper-service
RUN go mod download

RUN chmod +x /app/gatekeeper-service/entrypoint.sh

CMD ["/app/gatekeeper-service/entrypoint.sh"]