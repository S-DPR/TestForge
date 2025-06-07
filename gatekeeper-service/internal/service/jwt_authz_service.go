package service

import (
	"fmt"
	"github.com/golang-jwt/jwt/v5"
)

type JwtAuthzService struct {
}

type JwtAuthzServiceInterface interface {
	ValidateJwt(accessToken string) string
}

var jwtKey = []byte("django-insecure-q^o()$%1xke^3=gc0a@!%3og^l=yroxmswc74i*vp+-d@cc++p")

func NewJwtAuthzService() *JwtAuthzService {
	return &JwtAuthzService{}
}

func (j *JwtAuthzService) ValidateJwt(accessToken string) string {
	token, err := jwt.Parse(accessToken, func(token *jwt.Token) (interface{}, error) {
		if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
			return nil, fmt.Errorf("Unexpected signing method: %v", token.Header["alg"])
		}
		return jwtKey, nil
	})

	if err != nil {
		fmt.Println("토큰 검증 실패", err)
		return ""
	}

	if claims, ok := token.Claims.(jwt.MapClaims); ok && token.Valid {
		return claims["account_id"].(string)
	} else {
		return ""
	}
}
