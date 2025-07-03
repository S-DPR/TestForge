import {Button} from "@/components/ui/button";
import React, {useContext, useState} from "react";
import {TestcaseContext} from "@/context/TestcaseContext";
import PresetLoadModal from "@/components/preset/preset-load-modal";
import {HTTP_METHOD, LoginContext} from "@/context/LoginContext";

const PresetButton = () => {
  const ctx = useContext(TestcaseContext);
  const loginCtx = useContext(LoginContext);

  if (!ctx) throw new Error("context 없음. 개판임 ㅠ");
  if (!loginCtx) throw new Error("login Context error");

  const { blocks, preset } = ctx;
  const { request } = loginCtx;

  const [open, setOpen] = useState(false);

  const updatePreset = async () => {
    const req = {
      presetId: preset.presetId,
      presetName: preset.presetName,
      presetType: 'CUSTOM',
      content: JSON.stringify(blocks),
    }
    const response = await request({
      url: 'http://localhost:9001/preset',
      method: HTTP_METHOD.PUT,
      body: req,
    })
    const data = await response.json();
    return data;
  }

  return (
    <div className={"flex gap-3"}>
      <PresetLoadModal presetLoadModalOpen={open} setPresetLoadModalOpen={setOpen} />
      <Button
        size="sm"
        variant="secondary"
        onClick={() => setOpen(true)}
      >
        프리셋 불러오기
      </Button>
      <Button
        size="sm"
        variant="secondary"
        onClick={() => updatePreset()}
      >
        프리셋 저장하기
      </Button>
    </div>
  )
}

export default PresetButton;
