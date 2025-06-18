package handler

import (
	"bff/internal/service"
	"context"
	"github.com/gin-gonic/gin"
)

type StorageHandler struct {
	StorageHandlerService service.StorageServiceInterface
}

type StorageHandlerInterface interface {
	Read(c *gin.Context, filename string)
}

func NewStorageHandler(FileService service.StorageServiceInterface) *StorageHandler {
	return &StorageHandler{FileService}
}

func (h *StorageHandler) Read(c *gin.Context, filename string) {
	fileReadRes, err := h.StorageHandlerService.Read(filename, context.Background())
	if err != nil {
		c.Error(err)
		return
	}
	c.JSON(200, gin.H{
		"content": fileReadRes.Content,
	})
}
