import {Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle} from "@/components/ui/dialog";
import React, {useContext, useEffect, useState} from "react";
import {PresetSpec, TestcaseContext} from "@/context/TestcaseContext";
import {Input} from "@/components/ui/input";
import {Button} from "@/components/ui/button";
import {toast} from "sonner";
import {clsx} from "clsx";
import PresetPagination from "@/components/preset/preset-pagination";

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
  const [ currentPage, setCurrentPage ] = useState(0);
  const [ maxPage, setMaxPage ] = useState(0);

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
    if (response.status === 401) {
      toast.error("로그인이 필요합니다.", {
        style: {
          backgroundColor: "#FFB6C1",
          color: "#000000"
        }
      });
      return;
    }
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
      const response = await fetch(`http://localhost:9001/preset/search`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          size: 20,
          page: currentPage,
        }),
        credentials: "include"
      })
      const data = await response.json();
      setPresetData(data.presets);
      setMaxPage(data.maxPage);
    };
    innerFn();
  }, [presetLoadModalOpen, currentPage]);

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
