package model

import (
	"google.golang.org/protobuf/types/known/timestamppb"
)

type PresetCreateReqDTO struct {
	PresetName string `json:"preset_name"`
	PresetType string `json:"preset_type"`
	Content    string `json:"content"`
}

type PresetUpdateReqDTO struct {
	PresetId   string `json:"preset_id"`
	PresetName string `json:"preset_name"`
	PresetType string `json:"preset_type"`
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
	PresetId   string                 `json:"preset_id"`
	PresetName string                 `json:"preset_name"`
	PresetType string                 `json:"preset_type"`
	Content    string                 `json:"content"`
	AccountId  string                 `json:"account_id"`
	CreateDt   *timestamppb.Timestamp `json:"create_dt"`
	UpdateDt   *timestamppb.Timestamp `json:"update_dt"`
}

type PresetListResDTO struct {
	Presets []*PresetResDTO `json:"presets"`
}

type DeletePresetResDTO struct {
	Success bool `json:"success"`
}
