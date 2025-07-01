package model

import (
	"google.golang.org/protobuf/types/known/timestamppb"
)

type PresetCreateReqDTO struct {
	PresetName string `json:"presetName"`
	PresetType string `json:"presetType"`
	Content    string `json:"content"`
}

type PresetUpdateReqDTO struct {
	PresetId   string `json:"presetId"`
	PresetName string `json:"presetName"`
	PresetType string `json:"presetType"`
	Content    string `json:"content"`
}

type PresetIdReqDTO struct {
	PresetId string `json:"preset_id"`
}

type PresetListReqDTO struct {
	Page int32 `json:"page"`
	Size int32 `json:"size"`
}

type PresetResDTO struct {
	PresetId   string                 `json:"presetId"`
	PresetName string                 `json:"presetName"`
	PresetType string                 `json:"presetType"`
	Content    string                 `json:"content"`
	AccountId  string                 `json:"accountId"`
	CreateDt   *timestamppb.Timestamp `json:"createDt"`
	UpdateDt   *timestamppb.Timestamp `json:"updateDt"`
}

type PresetListResDTO struct {
	Presets []*PresetResDTO `json:"presets"`
}

type DeletePresetResDTO struct {
	Success bool `json:"success"`
}
