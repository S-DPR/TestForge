package model

type TestExecutorReqDTO struct {
	TestcaseFormat map[string]any `json:"testcaseFormat"`
	Code1          string         `json:"code1"`
	Code2          string         `json:"code2"`
	TimeLimit      int32          `json:"timeLimit"`
	RepeatCount    int32          `json:"repeatCount"`
}

type TestExecutorResDTO struct {
	filename   string
	diffStatus string
}
