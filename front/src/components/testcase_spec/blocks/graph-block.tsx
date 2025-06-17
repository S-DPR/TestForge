import {Label} from "@/components/ui/label";
import {Button} from "@/components/ui/button";
import VariableInput from "@/components/testcase_spec/variable-input";
import React, {useContext} from "react";
import {AbstractConfig, TestcaseContext} from "@/context/TestcaseContext";
import {Range} from "@/components/testcase_spec/define-range";
import {Checkbox} from "@/components/ui/checkbox";
import BlockWrapper from "@/components/testcase_spec/block-wrapper";

export interface GraphConfig extends AbstractConfig {
  nodeCount: string;
  edgeCount: string;
  weightRange: Range[];
  isPerfect: boolean;
  isConnect: boolean;
  isCycle: boolean;
}

interface GraphBlockProps {
  blockIndex: number;
}

const GraphBlock = ({ blockIndex }: GraphBlockProps) => {
  const ctx = useContext(TestcaseContext);
  if (!ctx) throw new Error('근데 이거 계속 반복되네');

  const { blocks, setBlocks } = ctx;
  const config: GraphConfig = blocks[blockIndex].config as GraphConfig;

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

      <div className="space-y-1">
        <Label className="text-sm text-gray-600">간선 개수</Label>
        <VariableInput
          value={config.edgeCount}
          blockIndex={blockIndex}
          showChar={false}
          variableIndex={10}
          onChange={(val) => updateConfig({ ...config, edgeCount: val })}
        />
      </div>
    </>
  )

  const specialSetting = (
    <>
      <div className="space-y-2">
        <Label className="text-sm text-gray-600">가중치 범위</Label>
        <div className="space-y-2">
          {config.weightRange.map((v, idx) => (
            <div key={`weight-range-${idx}`} className="flex gap-2">
              <VariableInput
                key={`weight-range-${idx}-min`}
                blockIndex={blockIndex}
                variableIndex={10}
                showChar={false}
                value={v.min}
                onChange={(val) =>
                  updateWeightRange(idx, { ...v, min: val })
                }
              />
              <VariableInput
                key={`weight-range-${idx}-max`}
                blockIndex={blockIndex}
                variableIndex={10}
                showChar={false}
                value={v.max}
                onChange={(val) =>
                  updateWeightRange(idx, { ...v, max: val })
                }
              />
            </div>
          ))}
        </div>
        <Button size="sm" onClick={addWeightRange}>
          수 범위 추가
        </Button>
      </div>

      <div className="space-y-2">
        <div className="flex items-center gap-2">
          <Checkbox
            checked={config.isPerfect}
            id="is-perfect"
            onCheckedChange={(chk) =>
              updateConfig({ ...config, isPerfect: !!chk.valueOf() })
            }
          />
          <Label htmlFor="is-perfect">완전그래프 여부</Label>
        </div>
        <div className="flex items-center gap-2">
          <Checkbox
            checked={config.isConnect}
            id="is-connect"
            onCheckedChange={(chk) =>
              updateConfig({ ...config, isConnect: !!chk.valueOf() })
            }
          />
          <Label htmlFor="is-connect">연결그래프 여부</Label>
        </div>
        <div className="flex items-center gap-2">
          <Checkbox
            checked={config.isCycle}
            id="is-cycle"
            onCheckedChange={(chk) =>
              updateConfig({ ...config, isCycle: !!chk.valueOf() })
            }
          />
          <Label htmlFor="is-cycle">사이클 여부</Label>
        </div>
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

export default GraphBlock;
