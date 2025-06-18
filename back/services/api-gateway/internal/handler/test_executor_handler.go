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

func (h *TestExecutorHandler) TestExecute(c *gin.Context, rateLimitService service.RateLimitService, req *model.TestExecutorReqDTO) {
	accountIdAny, exist := c.Get("accountId")
	if !exist {
		c.JSON(401, gin.H{"error": "account id not found"})
	}
	accountId := accountIdAny.(string)

	count := req.RepeatCount
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	if accountId == "" {
		c.JSON(401, gin.H{"error": "missing account-id header"})
		return
	}
	limitCheckRes, err := rateLimitService.Check(accountId, count, ctx)
	if err != nil {
		c.Error(err)
		return
	}
	if limitCheckRes.IsLimit {
		c.JSON(403, gin.H{
			"error": fmt.Sprintf("할당량 초과: %d회", limitCheckRes.AccCount),
		})
		return
	}

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

		if strings.Contains(payload["diffStatus"].(string), "EQUAL") {
			continue
		}
		return
	}
}
