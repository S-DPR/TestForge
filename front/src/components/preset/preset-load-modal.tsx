import {Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle} from "@/components/ui/dialog";
import React, {useContext, useEffect, useState} from "react";
import {BlockSpec, PresetSpec, TestcaseContext} from "@/context/TestcaseContext";
import {Input} from "@/components/ui/input";
import {Button} from "@/components/ui/button";

interface PresetLoadModalProps {
  presetLoadModalOpen: boolean;
  setPresetLoadModalOpen: (open: boolean) => void;
}

const PresetLoadModal = ({ presetLoadModalOpen, setPresetLoadModalOpen }: PresetLoadModalProps) => {
  const ctx = useContext(TestcaseContext);
  if (!ctx) throw new Error("context 없음. 개판임 ㅠ");

  const { blocks, setBlocks, preset, setPreset } = ctx;
  const [ presetData, setPresetData ] = useState<PresetSpec[]>([]);
  const [ search, setSearch ] = useState("");

  const savePreset = async (presetName: string) => {
    const request = {
      presetName: presetName,
      presetType: 'CUSTOM',
      content: JSON.stringify(blocks),
    }
    const response = await fetch('http://localhost:9001/preset', {
      method: 'POST',
      body: JSON.stringify(request),
      headers: {
        "Content-Type": "application/json",
      },
      credentials: 'include',
    })
    const data = await response.json();
    return data;
  }

  useEffect(() => {
    if (!presetLoadModalOpen) return;
    const innerFn = async () => {
      const response = await fetch(`http://localhost:9001/preset/search`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          size: 5,
          page: 0,
        }),
        credentials: "include"
      })
      const data = await response.json();
      setPresetData(data.presets);
    };
    innerFn();
  }, [presetLoadModalOpen])

  useEffect(() => {
    if (!preset.presetId) return;
    const innerFn = async () => {
      const response = await fetch(`http://localhost:9001/preset/${preset.presetId}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: "include"
      })
      const text = await response.text();
      const data = JSON.parse(text);
      setPreset(data);
      setBlocks(JSON.parse(data.content));
    };
    innerFn();
  }, [preset.presetId, setBlocks, setPreset])

  return (
    <Dialog open={presetLoadModalOpen} onOpenChange={setPresetLoadModalOpen}>
      <DialogContent className="sm:max-w-4xl">
        <DialogHeader>
          <DialogTitle>프리셋</DialogTitle>
          <DialogDescription>원하는 프리셋을 골라주세요.</DialogDescription>
          <div className="absolute top-4 right-4 flex gap-3">
            <Input value={search} onChange={e => setSearch(e.target.value)} placeholder="프리셋 이름" />
            <Button onClick={() => savePreset(search)}>새로 만들기</Button>
          </div>
        </DialogHeader>

        <div className="grid grid-cols-5 gap-4">
        {presetData.map((item, i) => (
          <div
            key={i}
            className= "h-12 flex items-center justify-center font-semibold rounded-lg shadow-sm cursor-pointer hover:brightness-95 transition"
            onClick={() => {
              setPreset(item);
              setPresetLoadModalOpen(false);
            }}
          >
            {item.presetName}
          </div>
        ))}
        </div>
      </DialogContent>
    </Dialog>
  )
}

export default PresetLoadModal;
