import {Button} from "@/components/ui/button";
import {Popover, PopoverContent, PopoverTrigger} from "@/components/ui/popover";
import {Command, CommandEmpty} from "@/components/ui/command";
import React, {useContext, useEffect, useState} from "react";
import {TestcaseContext} from "@/context/TestcaseContext";
import {CommandInput} from "cmdk";

const PresetAddButton = () => {
  const ctx = useContext(TestcaseContext);
  if (!ctx) throw new Error("context 없음. 개판임 ㅠ");

  const { blocks, setBlocks, preset, setPreset } = ctx;

  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState<Record<string, string>>({});
  const [input, setInput] = useState("");
  const [presetName, setPresetName] = useState<string>("");

  const savePreset = () => {
    setPreset(prev => {
      const newPreset = structuredClone(prev);
      newPreset.content = blocks;
      return newPreset;
    })
  }

  useEffect(() => {
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
      setBlocks(data.content);
    };
    innerFn();
  }, [preset.presetId, setBlocks, setPreset])

  return (
    <>
      <Popover open={open} onOpenChange={setOpen}>
        <PopoverTrigger asChild>
          <Button variant="outline" className="w-[280px] justify-start text-sm text-gray-800 bg-white hover:bg-gray-50 border-gray-300">
            {presetName || "값 선택 또는 입력"}
          </Button>
        </PopoverTrigger>
        <PopoverContent className="w-[280px] p-0 bg-white border border-gray-200 shadow-md rounded-md z-50 max-h-[300px] overflow-y-auto">
          <Command>
            <CommandInput
              placeholder="프리셋 이름 입력..."
              value={input}
              onValueChange={(val) => {
                setInput(val)
                setPresetName(val)
              }}
            />
            <CommandEmpty>결과 없음. Enter로 직접 입력 가능</CommandEmpty>
          </Command>
        </PopoverContent>
      </Popover>
      <Button
        size="sm"
        variant="secondary"
        onClick={() => setPreset({...preset, presetId})}
      >
        프리셋 불러오기
      </Button>
      <Button
        size="sm"
        variant="secondary"
        onClick={() => savePreset()}
      >
        프리셋 저장하기
      </Button>
    </>
  )
}

export default PresetAddButton;
