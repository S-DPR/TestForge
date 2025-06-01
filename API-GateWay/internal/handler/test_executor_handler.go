package handler

import (
	"bff/internal/model"
	"bff/internal/service"
	"encoding/json"
	"fmt"
	"github.com/gin-gonic/gin"
	"io"
)

type TestExecutorHandler struct {
	TestExecutorService service.TestExecutorServiceInterface
}

type TestExecutorHandlerInterface interface {
	TestExecute(c *gin.Context, req *model.TestExecutorReqDTO)
}

func NewTestExecutorHandler(TestExecutorService service.TestExecutorServiceInterface) *TestExecutorHandler {
	return &TestExecutorHandler{TestExecutorService}
}

func (h *TestExecutorHandler) TestExecute(c *gin.Context, req *model.TestExecutorReqDTO) {
	stream, err := h.TestExecutorService.TestExecute(req)
	if err != nil {
		c.Error(err)
		return
	}

	c.Writer.Header().Set("Content-Type", "text/event-stream") // SSE MIME type
	c.Writer.Header().Set("Cache-Control", "no-cache")
	c.Writer.Header().Set("Connection", "keep-alive")
	for {
		msg, err := stream.Recv()
		if err == io.EOF {
			break
		}
		if err != nil {
			c.Error(err)
			return
		}

		payload := gin.H{
			"filename":   msg.Filename,
			"diffStatus": msg.DiffStatus,
		}

		// JSON 직렬화
		jsonData, err := json.Marshal(payload)
		if err != nil {
			c.Error(err)
			return
		}

		// SSE 포맷으로 전송
		fmt.Fprintf(c.Writer, "data: %s\n\n", jsonData)
		c.Writer.Flush()
	}
}
