package handler

import (
	"bff/internal/model"
	"bff/internal/service"
	"context"
	"fmt"
	"github.com/gin-gonic/gin"
	"io"
	"strings"
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
	//ctx, cancel := context.WithCancel(context.Background())
	ctx := c.Request.Context()
	c.Request.Context()

	stream, err := h.TestExecutorService.TestExecute(req, ctx)
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
		//jsonData, err := json.Marshal(payload)
		//if err != nil {
		//	c.Error(err)
		//	cancel()
		//	return
		//}

		// SSE 포맷으로 전송
		c.SSEvent("message", payload)
		fmt.Fprintf(c.Writer, "data: %s\n\n", payload)
		c.Writer.Flush()

		//if strings.Contains(payload["diffStatus"].(string), "EQUAL") {
		//	continue
		//}
		continue
		return
	}
}
