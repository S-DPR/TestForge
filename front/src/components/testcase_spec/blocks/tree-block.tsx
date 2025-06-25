import {Label} from "@/components/ui/label";
import {Button} from "@/components/ui/button";
import VariableInput from "@/components/testcase_spec/variable-input";
import React, {useContext} from "react";
import {AbstractConfig, TestcaseContext} from "@/context/TestcaseContext";
import DefineRange, {Range} from "@/components/testcase_spec/define-range";
import {Checkbox} from "@/components/ui/checkbox";
import BlockWrapper from "@/components/testcase_spec/block-wrapper";
import {Card} from "@/components/ui/card";

export interface GraphConfig extends AbstractConfig {
  nodeCount: string;
  edgeCount: string;
  weightRange: Range[];
  isPerfect: boolean;
  isConnect: boolean;
  isCycle: boolean;
}

interface TreeBlockProps {
  blockIndex: number;
}

const TreeBlock = ({ blockIndex }: TreeBlockProps) => {
  const ctx = useContext(TestcaseContext);
  if (!ctx) throw new Error('근데 이거 계속 반복되네');

  const { blocks, setBlocks } = ctx;
  const config: GraphConfig = blocks[blockIndex].config as GraphConfig;

  config.isConnect = true;
  config.isCycle = false;
  config.isPerfect = false;

  const updateConfig = (config: GraphConfig) => {
    setBlocks((prev) => {
      const newBlocks = structuredClone(prev);
      newBlocks[blockIndex].config = config;
      return newBlocks;
    })
  }

  const updateWeightRange = (rangeIndex: number, range: Range) => {
    setBlocks((prev) => {
      const newBlocks = structuredClone(prev);
      const cfg: GraphConfig = newBlocks[blockIndex].config as GraphConfig;
      cfg.weightRange[rangeIndex] = range;
      return newBlocks;
    })
  }

  const deleteWeightRange = (rangeIndex: number) => {
    setBlocks((prev) => {
      const newBlocks = structuredClone(prev);
      const cfg: GraphConfig = newBlocks[blockIndex].config as GraphConfig;
      cfg.weightRange = cfg.weightRange.filter((_, idx) => idx !== rangeIndex);
      return newBlocks;
    })
  }

  const addWeightRange = () => {
    setBlocks((prev) => {
      const newBlocks = structuredClone(prev);
      const cfg: GraphConfig = newBlocks[blockIndex].config as GraphConfig;
      cfg.weightRange.push({ min: '0', max: '10' })
      return newBlocks;
    })
  }

  const defaultSetting = (
    <>
      <div className="space-y-1">
        <Label className="text-sm text-gray-600">노드 개수</Label>
        <VariableInput
          value={config.nodeCount}
          blockIndex={blockIndex}
          showChar={false}
          variableIndex={10}
          onChange={(val) => updateConfig({ ...config, nodeCount: val })}
        />
      </div>
    </>
  )

  const specialSetting = (
    <>
      <div className="space-y-2">
        <Card className="p-4 rounded-2xl shadow-md border border-gray-200 bg-white space-y-3">
          <Label className="text-sm text-gray-600">가중치 범위</Label>
          <div className="space-y-2">
            {config.weightRange.map((v, idx) => (
              <DefineRange
                key={idx}
                blockIndex={blockIndex}
                variableIndex={10}
                minValue={v.min}
                maxValue={v.max}
                onMinChange={(val) => updateWeightRange(idx, { ...v, min: val })}
                onMaxChange={(val) => updateWeightRange(idx, { ...v, max: val })}
                onDeleteClick={() => deleteWeightRange(idx)}
              />
            ))}
          </div>
          <div className="flex pt-4 justify-center">
            <Button size="sm" onClick={addWeightRange}>
              수 범위 추가
            </Button>
          </div>
        </Card>
      </div>
    </>
  )

  return (
    <BlockWrapper
      blockIndex={blockIndex}
      defaultSetting={defaultSetting}
      specialSetting={specialSetting}
      isRenderOutput={true}
    />)
}

export default TreeBlock;
