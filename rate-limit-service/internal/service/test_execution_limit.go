package service

import (
	"context"
	"fmt"
	"github.com/redis/go-redis/v9"
)

var ctx = context.Background()

func IsRateLimited() {
	rdb := redis.NewClient(&redis.Options{
		Addr:     "redis:6379",
		Password: "",
		DB:       0,
	})

	err := rdb.Set(ctx, "mykey", "hello", 0).Err()
	if err != nil {
		panic(err)
	}

	val, err := rdb.Get(ctx, "mykey").Result()
	if err != nil {
		panic(err)
	}

	fmt.Println("mykey:", val)
}
