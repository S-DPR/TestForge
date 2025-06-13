import {Card} from "@/components/ui/card";
import {Label} from "@/components/ui/label";
import {Button} from "@/components/ui/button";
import Variable from "@/components/testcase_spec/variable";
import VariableInput from "@/components/testcase_spec/variable-input";
import React, {useContext} from "react";
import {AbstractConfig, TestcaseContext} from "@/context/TestcaseContext";
import Output from "@/components/testcase_spec/output";
import {Range} from "@/components/testcase_spec/define-range";
import {Checkbox} from "@/components/ui/checkbox";

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

  const { blocks, setBlocks, addVariable, updateBlockRepeat } = ctx;
  const currentBlock = blocks[blockIndex]
  const currentVariable = currentBlock.variables;
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

  return (
    <Card className="p-6 space-y-6 bg-white border border-gray-200 rounded-lg shadow-sm">
      {/* 반복 횟수 */}
      <div className="space-y-1">
        <Label className="text-sm text-gray-700">반복 횟수</Label>
        <VariableInput
          value={currentBlock.repeat}
          onChange={(val) => updateBlockRepeat(blockIndex, val)}
          showChar={false}
          blockIndex={blockIndex - 1}
          variableIndex={10}
        />
      </div>

      {/* 변수 설정 */}
      <div className="space-y-2">
        <Label className="text-sm text-gray-700">변수 설정</Label>
        <div className="space-y-2">
          {currentVariable.map((v, idx) =>
              !v.isReserved && (
                <Variable
                  key={`${blockIndex}-variable-${idx}`}
                  blockIndex={blockIndex}
                  variableIndex={idx}
                />
              )
          )}
        </div>
        <Button
          size="sm"
          variant="outline"
          onClick={() =>
            addVariable(blockIndex, {
              name: "",
              type: "",
              ranges: [],
              isReserved: false,
            })
          }
        >
          변수 추가
        </Button>
      </div>

      {/* 그래프 상세 설정 */}
      <div className="space-y-4">
        <Label className="text-sm text-gray-700">그래프 상세 설정</Label>

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
      </div>

      {/* Output */}
      <div>
        <Label className="text-sm text-gray-700">출력 설정</Label>
        <Output blockIndex={blockIndex} />
      </div>
    </Card>
  )
}

export default GraphBlock;
