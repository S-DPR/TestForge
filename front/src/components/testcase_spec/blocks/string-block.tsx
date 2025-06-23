import {Label} from "@/components/ui/label";
import {Button} from "@/components/ui/button";
import VariableInput from "@/components/testcase_spec/variable-input";
import React, {useContext} from "react";
import {TestcaseContext} from "@/context/TestcaseContext";
import DefineRange, {Range} from "@/components/testcase_spec/define-range";
import {Checkbox} from "@/components/ui/checkbox";
import {MatrixConfig} from "@/components/testcase_spec/blocks/matrix-block";
import BlockWrapper from "@/components/testcase_spec/block-wrapper";
import { Card } from "@/components/ui/card";

interface StringBlockProps {
  blockIndex: number;
}

const StringBlock = ({ blockIndex }: StringBlockProps) => {
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

  const deleteNumRange = (numRangeIndex: number) => {
    setBlocks((prev) => {
      const newBlocks = structuredClone(prev);
      const cfg: MatrixConfig = newBlocks[blockIndex].config as MatrixConfig;
      cfg.numRange = cfg.numRange.filter((_, idx) => idx !== numRangeIndex);
      return newBlocks;
    })
  }

  config.numType = 'char';

  const defaultSetting = (
    <>
      <div className="space-y-1">
        <Label className="text-sm text-gray-600">문자열 길이</Label>
        <VariableInput
          value={config.colSize}
          blockIndex={blockIndex}
          showChar={false}
          variableIndex={10}
          onChange={(val) => updateConfig({ ...config, colSize: val })}
        />

        <Card className="p-4 rounded-2xl shadow-md border border-gray-200 bg-white">
          <div className="space-y-2">
            <Label className="text-sm text-gray-600">아스키코드 범위</Label>
            <div className="space-y-2">
              {config.numRange.map((v, idx) => (
                <DefineRange
                  key={idx}
                  blockIndex={blockIndex}
                  variableIndex={10}
                  minValue={v.min}
                  maxValue={v.max}
                  onMinChange={(val) => updateNumRange(idx, { ...v, min: val })}
                  onMaxChange={(val) => updateNumRange(idx, { ...v, max: val })}
                  onDeleteClick={() => deleteNumRange(idx)}
                />
              ))}
            </div>
            <div className={"flex justify-center"}>
              <Button size="sm" onClick={addNumRange}>
                수 범위 추가
              </Button>
            </div>
          </div>
        </Card>
      </div>
    </>
  )
  const specialSetting = (
    <>
      {/* 체크박스 그룹 */}
      <div className="space-y-2">
        {[
          ["isDistinct", "중복 없는 문자열"],
          ["randomEmpty", "랜덤한 위치 비우기"],
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

export default StringBlock;
