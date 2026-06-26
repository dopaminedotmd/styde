user/models.go
package models
type User struct {
    ID        string `json:"id"`
    Email     string `json:"email"`
    Name      string `json:"name"`
    CreatedAt int64  `json:"created_at"`
}
type CreateUserRequest struct {
    Email string `json:"email"`
    Name  string `json:"name"`
}
type GetUserRequest struct {
    ID string `json:"id"`
}
proto/user/v1/user.proto
syntax = "proto3";
package user.v1;
option go_package = "github.com/example/user-service/gen/user/v1;userpb";
service UserService {
    rpc CreateUser(CreateUserRequest) returns (CreateUserResponse);
    rpc GetUser(GetUserRequest) returns (GetUserResponse);
}
message CreateUserRequest {
    string email = 1;
    string name = 2;
}
message CreateUserResponse {
    string id = 1;
}
message GetUserRequest {
    string id = 1;
}
message GetUserResponse {
    string id = 1;
    string email = 2;
    string name = 3;
    int64 created_at = 4;
}
internal/server/grpc.go
package server
import (
    "context"
    "fmt"
    "net"
    "google.golang.org/grpc"
    "google.golang.org/grpc/reflection"
    "github.com/example/user-service/internal/service"
    userpb "github.com/example/user-service/gen/user/v1"
)
type GRPCServer struct {
    server *grpc.Server
    svc    *service.UserService
    userpb.UnimplementedUserServiceServer
}
func NewGRPCServer(svc *service.UserService) *GRPCServer {
    s := grpc.NewServer(
        grpc.UnaryInterceptor(unaryInterceptor),
    )
    gs := &GRPCServer{server: s, svc: svc}
    userpb.RegisterUserServiceServer(s, gs)
    reflection.Register(s)
    return gs
}
func (g *GRPCServer) CreateUser(ctx context.Context, req *userpb.CreateUserRequest) (*userpb.CreateUserResponse, error) {
    return g.svc.CreateUser(ctx, req)
}
func (g *GRPCServer) GetUser(ctx context.Context, req *userpb.GetUserRequest) (*userpb.GetUserResponse, error) {
    return g.svc.GetUser(ctx, req)
}
func (g *GRPCServer) Serve(addr string) error {
    lis, err := net.Listen("tcp", addr)
    if err != nil {
        return fmt.Errorf("listen %s: %w", addr, err)
    }
    return g.server.Serve(lis)
}
func (g *GRPCServer) GracefulStop() {
    g.server.GracefulStop()
}
func unaryInterceptor(ctx context.Context, req interface{}, info *grpc.UnaryServerInfo, handler grpc.UnaryHandler) (interface{}, error) {
    resp, err := handler(ctx, req)
    return resp, err
}
internal/repository/user_repo.go
package repository
import (
    "context"
    "sync"
    "time"
    "github.com/example/user-service/internal/models"
)
type UserRepository struct {
    mu    sync.RWMutex
    users map[string]*models.User
}
func NewUserRepository() *UserRepository {
    return &UserRepository{
        users: make(map[string]*models.User),
    }
}
func (r *UserRepository) Save(ctx context.Context, u *models.User) error {
    r.mu.Lock()
    defer r.mu.Unlock()
    r.users[u.ID] = u
    return nil
}
func (r *UserRepository) FindByID(ctx context.Context, id string) (*models.User, error) {
    r.mu.RLock()
    defer r.mu.RUnlock()
    u, ok := r.users[id]
    if !ok {
        return nil, ErrNotFound
    }
    return u, nil
}
internal/service/user_service.go
package service
import (
    "context"
    "fmt"
    "time"
    "crypto/rand"
    "encoding/hex"
    userpb "github.com/example/user-service/gen/user/v1"
    "github.com/example/user-service/internal/models"
    "github.com/example/user-service/internal/repository"
)
type UserService struct {
    repo    *repository.UserRepository
    workers chan struct{}
}
func NewUserService(repo *repository.UserRepository) *UserService {
    return &UserService{
        repo:    repo,
        workers: make(chan struct{}, 10),
    }
}
func (s *UserService) CreateUser(ctx context.Context, req *userpb.CreateUserRequest) (*userpb.CreateUserResponse, error) {
    select {
    case s.workers <- struct{}{}:
        defer func() { <-s.workers }()
    default:
        return nil, fmt.Errorf("too many concurrent requests")
    }
    id, err := generateID()
    if err != nil {
        return nil, fmt.Errorf("generate id: %w", err)
    }
    user := &models.User{
        ID:        id,
        Email:     req.Email,
        Name:      req.Name,
        CreatedAt: time.Now().Unix(),
    }
    if err := s.repo.Save(ctx, user); err != nil {
        return nil, fmt.Errorf("save user: %w", err)
    }
    return &userpb.CreateUserResponse{Id: user.ID}, nil
}
func (s *UserService) GetUser(ctx context.Context, req *userpb.GetUserRequest) (*userpb.GetUserResponse, error) {
    user, err := s.repo.FindByID(ctx, req.Id)
    if err != nil {
        return nil, err
    }
    return &userpb.GetUserResponse{
        Id:        user.ID,
        Email:     user.Email,
        Name:      user.Name,
        CreatedAt: user.CreatedAt,
    }, nil
}
func generateID() (string, error) {
    b := make([]byte, 16)
    if _, err := rand.Read(b); err != nil {
        return "", err
    }
    return hex.EncodeToString(b), nil
}
cmd/server/main.go
package main
import (
    "context"
    "log"
    "os"
    "os/signal"
    "syscall"
    "github.com/example/user-service/internal/server"
    "github.com/example/user-service/internal/service"
    "github.com/example/user-service/internal/repository"
)
func main() {
    ctx, cancel := context.WithCancel(context.Background())
    defer cancel()
    repo := repository.NewUserRepository()
    svc := service.NewUserService(repo)
    grpcServer := server.NewGRPCServer(svc)
    errCh := make(chan error, 1)
    go func() {
        addr := ":50051"
        log.Printf("gRPC server listening on %s", addr)
        if err := grpcServer.Serve(addr); err != nil {
            errCh <- err
        }
    }()
    sigCh := make(chan os.Signal, 1)
    signal.Notify(sigCh, syscall.SIGINT, syscall.SIGTERM)
    select {
    case sig := <-sigCh:
        log.Printf("received signal %v, shutting down", sig)
    case err := <-errCh:
        log.Printf("server error: %v", err)
    case <-ctx.Done():
    }
    grpcServer.GracefulStop()
    log.Println("server stopped")
}
internal/service/user_service_test.go
package service
import (
    "context"
    "testing"
    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/require"
    userpb "github.com/example/user-service/gen/user/v1"
    "github.com/example/user-service/internal/repository"
)
func TestUserService_CreateUser(t *testing.T) {
    tests := []struct {
        name    string
        req     *userpb.CreateUserRequest
        wantErr bool
    }{
        {
            name: "valid user",
            req: &userpb.CreateUserRequest{
                Email: "test@example.com",
                Name:  "Test User",
            },
            wantErr: false,
        },
        {
            name: "empty email",
            req: &userpb.CreateUserRequest{
                Email: "",
                Name:  "No Email",
            },
            wantErr: false,
        },
    }
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            repo := repository.NewUserRepository()
            svc := NewUserService(repo)
            got, err := svc.CreateUser(context.Background(), tt.req)
            if tt.wantErr {
                assert.Error(t, err)
                return
            }
            require.NoError(t, err)
            assert.NotEmpty(t, got.Id)
        })
    }
}
func TestUserService_GetUser(t *testing.T) {
    repo := repository.NewUserRepository()
    svc := NewUserService(repo)
    created, err := svc.CreateUser(context.Background(), &userpb.CreateUserRequest{
        Email: "get@example.com",
        Name:  "Get Test",
    })
    require.NoError(t, err)
    tests := []struct {
        name    string
        id      string
        wantErr bool
    }{
        {
            name:    "existing user",
            id:      created.Id,
            wantErr: false,
        },
        {
            name:    "not found",
            id:      "nonexistent",
            wantErr: true,
        },
    }
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got, err := svc.GetUser(context.Background(), &userpb.GetUserRequest{Id: tt.id})
            if tt.wantErr {
                assert.Error(t, err)
                assert.Nil(t, got)
                return
            }
            require.NoError(t, err)
            assert.Equal(t, tt.id, got.Id)
            assert.Equal(t, "get@example.com", got.Email)
        })
    }
}
internal/repository/errors.go
package repository
import "errors"
var ErrNotFound = errors.New("user not found")
wire.go
//go:build wireinject
// +build wireinject
package main
import (
    "github.com/google/wire"
    "github.com/example/user-service/internal/server"
    "github.com/example/user-service/internal/service"
    "github.com/example/user-service/internal/repository"
)
func InitializeServer() (*server.GRPCServer, error) {
    wire.Build(
        repository.NewUserRepository,
        service.NewUserService,
        server.NewGRPCServer,
    )
    return nil, nil
}
wire_gen.go
// Code generated by Wire. DO NOT EDIT.
//go:build !wireinject
// +build !wireinject
package main
import (
    "github.com/example/user-service/internal/server"
    "github.com/example/user-service/internal/service"
    "github.com/example/user-service/internal/repository"
)
func InitializeServer() (*server.GRPCServer, error) {
    repo := repository.NewUserRepository()
    userService := service.NewUserService(repo)
    grpcServer := server.NewGRPCServer(userService)
    return grpcServer, nil
}
Dockerfile
FROM golang:1.22-alpine AS builder
WORKDIR /src
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o /app ./cmd/server/
FROM scratch
COPY --from=builder /app /app
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
EXPOSE 50051
ENTRYPOINT ["/app"]
go.mod
module github.com/example/user-service
go 1.22
require (
    google.golang.org/grpc v1.64.0
    google.golang.org/protobuf v1.34.1
    github.com/google/wire v0.6.0
    github.com/stretchr/testify v1.9.0
)
makefile
.PHONY: proto gen test build docker
proto:
    protoc --go_out=. --go_opt=paths=source_relative \
        --go-grpc_out=. --go-grpc_opt=paths=source_relative \
        proto/user/v1/user.proto
gen:
    cd cmd/server && wire
test:
    go test -v -race -count=1 ./...
build:
    go build -o bin/server ./cmd/server/
docker:
    docker build -t user-service:latest .
run:
    go run ./cmd/server/
Goroutine pattern: worker pool (channel buffered to 10) limits concurrent creates.
gRPC: protobuf service with unary interceptor, reflection enabled.
DI: Wire generates wire_gen.go from wire.go.
Test: table-driven with testify assert/require.
Docker: scratch image, CGO disabled, ssl certs included.