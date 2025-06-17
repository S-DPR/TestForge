import {Label} from "@/components/ui/label";
import {Button} from "@/components/ui/button";
import VariableInput from "@/components/testcase_spec/variable-input";
import React, {useContext} from "react";
import {AbstractConfig, TestcaseContext} from "@/context/TestcaseContext";
import {Range} from "@/components/testcase_spec/define-range";
import {Checkbox} from "@/components/ui/checkbox";
import {Select, SelectContent, SelectGroup, SelectItem, SelectTrigger, SelectValue} from "@/components/ui/select";
import BlockWrapper from "@/components/testcase_spec/block-wrapper";

export interface MatrixConfig extends AbstractConfig {
  colSize: string;
  rowSize: string;
  numType: string;
  numRange: Range[];
  isDistinct: boolean;
  valueLimit: Record<string, number>;
  emptyValue: string | null;
  randomEmpty: boolean;
  isGraph: boolean;
  isSymmetric: boolean;
}

interface MatrixBlockProps {
  blockIndex: number;
}

const MatrixBlock = ({ blockIndex }: MatrixBlockProps) => {
  const ctx = useContext(TestcaseContext);
  if (!ctx) throw new Error('근데 이거 계속 반복되네');

  const { blocks, setBlocks } = ctx;
  const config: MatrixConfig = blocks[blockIndex].config as MatrixConfig;

  const updateConfig = (config: MatrixConfig) => {
    setBlocks((prev) => {
      const newBlocks = structuredClone(prev);
      newBlocks[blockIndex].config = config;
      return newBlocks;
    })
  }

  const updateNumRange = (weightRangeIndex: number, range: Range) => {
    setBlocks((prev) => {
      const newBlocks = structuredClone(prev);
      const cfg: MatrixConfig = newBlocks[blockIndex].config as MatrixConfig;
      cfg.numRange[weightRangeIndex] = range;
      return newBlocks;
    })
  }

  const addNumRange = () => {
    setBlocks((prev) => {
      const newBlocks = structuredClone(prev);
      const cfg: MatrixConfig = newBlocks[blockIndex].config as MatrixConfig;
      cfg.numRange.push({ min: '0', max: '0' });
      return newBlocks;
    })
  }

  const defaultSetting = (
    <>
      <div className="space-y-1">
        <Label className="text-sm text-gray-600">가로 길이</Label>
        <VariableInput
          value={config.colSize}
          blockIndex={blockIndex}
          showChar={false}
          variableIndex={10}
          onChange={(val) => updateConfig({ ...config, colSize: val })}
        />
      </div>

      <div className="space-y-1">
        <Label className="text-sm text-gray-600">세로 길이</Label>
        <VariableInput
          value={config.rowSize}
          blockIndex={blockIndex}
          showChar={false}
          variableIndex={10}
          onChange={(val) => updateConfig({ ...config, rowSize: val })}
        />
      </div>

      <div className="space-y-1">
        <Label className="text-sm text-gray-600">내부 타입</Label>
        <Select
          value={config.numType}
          onValueChange={(val) => updateConfig({ ...config, numType: val })}
        >
          <SelectTrigger className="w-[180px] border-gray-300 rounded-md px-3 py-2 text-sm">
            <SelectValue placeholder="변수 타입" />
          </SelectTrigger>
          <SelectContent className="bg-white border border-gray-200 shadow-md rounded-md">
            <SelectGroup>
              <SelectItem value="int">Number</SelectItem>
              <SelectItem value="char">Char</SelectItem>
              <SelectItem value="enum">Enum</SelectItem>
            </SelectGroup>
          </SelectContent>
        </Select>
      </div>

      <div className="space-y-2">
        <Label className="text-sm text-gray-600">수 범위</Label>
        <div className="space-y-2">
          {config.numRange.map((v, idx) => (
            <div key={idx} className="flex gap-2">
              <VariableInput
                blockIndex={blockIndex}
                variableIndex={10}
                showChar={false}
                value={v.min}
                onChange={(val) =>
                  updateNumRange(idx, { ...v, min: val })
                }
              />
              <VariableInput
                blockIndex={blockIndex}
                variableIndex={10}
                showChar={false}
                value={v.max}
                onChange={(val) =>
                  updateNumRange(idx, { ...v, max: val })
                }
              />
            </div>
          ))}
        </div>
        <Button size="sm" onClick={addNumRange}>
          수 범위 추가
        </Button>
      </div>
    </>
  )

  const specialSetting = (
    <>
      <div className="space-y-2">
        {[
          ["isDistinct", "중복 없는 행렬"],
          ["randomEmpty", "랜덤한 위치 비우기"],
          ["isGraph", "행렬그래프 여부"],
          ["isSymmetric", "대칭행렬 여부"]
        ].map(([key, label]) => (
          <div key={key} className="flex items-center gap-2">
            <Checkbox
              checked={(config as any)[key]}
              id={key}
              onCheckedChange={(chk) =>
                updateConfig({ ...config, [key]: !!chk.valueOf() })
              }
            />
            <Label htmlFor={key}>{label}</Label>
          </div>
        ))}
      </div>
    </>
  )
  return (
    <BlockWrapper
      blockIndex={blockIndex}
      defaultSetting={defaultSetting}
      specialSetting={specialSetting}
      isRenderOutput={true}
    />
  )
}

export default MatrixBlock;
