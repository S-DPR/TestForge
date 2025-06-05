package service

import (
	"context"
	"errors"
	"github.com/redis/go-redis/v9"
	"strconv"
)

type TestExecutionLimitService struct {
	ctx context.Context
	rdb *redis.Client
}

type TestExecutionLimitServiceInterface interface {
	IsRateLimited(accountId string, count int) bool
}

const MaxExecutionsPerDay = 3000

func NewTestExecutionLimitService(ctx context.Context, rdb *redis.Client) TestExecutionLimitService {
	return TestExecutionLimitService{ctx: ctx, rdb: rdb}
}

func (t *TestExecutionLimitService) IsRateLimited(accountId string, count int32) (bool, int32) {
	val, err := t.rdb.Get(t.ctx, accountId).Result()
	if errors.Is(err, redis.Nil) {
		val = "0"
	} else if err != nil {
		panic(err)
	}
	currentCount, err := strconv.Atoi(val)
	if err != nil {
		panic(err)
	}

	newCount := int32(currentCount) + count

	erro := t.rdb.Set(t.ctx, accountId, newCount, 0).Err()
	if erro != nil {
		panic(erro)
	}

	return newCount <= MaxExecutionsPerDay, newCount
}
