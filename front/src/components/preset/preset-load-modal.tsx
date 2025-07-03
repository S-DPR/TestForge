import {Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle} from "@/components/ui/dialog";
import React, {useContext, useEffect, useState} from "react";
import {PresetSpec, TestcaseContext} from "@/context/TestcaseContext";
import {Input} from "@/components/ui/input";
import {Button} from "@/components/ui/button";
import {clsx} from "clsx";
import PresetPagination from "@/components/preset/preset-pagination";
import {HTTP_METHOD, LoginContext} from "@/context/LoginContext";

interface PresetLoadModalProps {
  presetLoadModalOpen: boolean;
  setPresetLoadModalOpen: (open: boolean) => void;
}

const PresetLoadModal = ({ presetLoadModalOpen, setPresetLoadModalOpen }: PresetLoadModalProps) => {
  const ctx = useContext(TestcaseContext);
  const loginCtx = useContext(LoginContext);
  if (!ctx) throw new Error("context 없음. 개판임 ㅠ");
  if (!loginCtx) throw new Error("login context error");

  const { blocks, setBlocks, preset, setPreset } = ctx;
  const { request } = loginCtx;
  const [ presetData, setPresetData ] = useState<PresetSpec[]>([]);
  const [ search, setSearch ] = useState("");
  const [ currentPage, setCurrentPage ] = useState(0);
  const [ maxPage, setMaxPage ] = useState(0);

  const savePreset = async (presetName: string) => {
    const req = {
      presetName: presetName,
      presetType: 'CUSTOM',
      content: JSON.stringify(blocks),
    }
    const response = await request({
      url: 'http://localhost:9001/preset',
      method: HTTP_METHOD.POST,
      body: req,
    })
    const data = await response.json();
    setPresetData(prev => {
      let newPresetData = [data, ...prev];
      newPresetData = newPresetData.slice(0, 20);
      return newPresetData;
    })
    return data;
  }

  useEffect(() => {
    if (!presetLoadModalOpen) return;
    const innerFn = async () => {
      const response = await request({
        url: `http://localhost:9001/preset/search`,
        method: HTTP_METHOD.POST,
        body: { size: 20, page: currentPage },
      })
      const data = await response.json();
      setPresetData(data.presets);
      setMaxPage(data.maxPage);
    };
    innerFn();
  }, [presetLoadModalOpen, currentPage, request]);

  useEffect(() => {
    if (!preset.presetId) return;
    const innerFn = async () => {
      const response = await request({
        url: `http://localhost:9001/preset/${preset.presetId}`,
        method: HTTP_METHOD.GET,
      })
      const text = await response.text();
      const data = JSON.parse(text);
      setPreset(data);
      setBlocks(JSON.parse(data.content));
    };
    innerFn();
  }, [preset.presetId, setBlocks, setPreset])

  const getCardColor = (type: string): string => {
    switch (type) {
      case "CUSTOM":
        return "bg-blue-50 border border-blue-300";
      case "BAEKJOON":
        return "bg-green-50 border border-green-300";
      default:
        return "bg-orange-50 border border-orange-300";
    }
  };

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
            className= {clsx("h-12 flex items-center justify-center font-semibold rounded-lg shadow-sm cursor-pointer hover:brightness-95 transition", getCardColor(item.presetType))}
            onClick={() => {
              setPreset(item);
              setPresetLoadModalOpen(false);
            }}
          >
            {item.presetName}
          </div>
        ))}
        </div>

        <PresetPagination maxPages={maxPage} currentPage={currentPage} setCurrentPage={setCurrentPage} />
      </DialogContent>
    </Dialog>
  )
}

export default PresetLoadModal;
