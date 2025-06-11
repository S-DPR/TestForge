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

  const { blocks, setBlocks, addVariable } = ctx;
  const currentVariable = blocks[blockIndex].variables;
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
    <div>
      <Card>
        <Card>
          <Label>반복 횟수</Label>
          <VariableInput blockIndex={blockIndex-1} variableIndex={10}></VariableInput>
        </Card>
        <Card>
          <Label>변수 설정</Label>
          {currentVariable.map((v, idx) => !v.isReserved && (
            <Variable
              key={`${blockIndex}-variable-${idx}`}
              blockIndex={blockIndex}
              variableIndex={idx}
            />
          ))}
          <Button onClick={() => addVariable(blockIndex, {name: '', type: '', ranges: [], isReserved: false})}>변수 추가</Button>
        </Card>
        <Card>
          <Label>상세 설정</Label>

          <Label>노드 개수</Label>
          <VariableInput initValue={config.nodeCount} blockIndex={blockIndex} variableIndex={10} onChange={(val) => { updateConfig({...config, nodeCount: val}) }} />

          <Label>간선 개수</Label>
          <VariableInput initValue={config.edgeCount} blockIndex={blockIndex} variableIndex={10} onChange={(val) => { updateConfig({...config, edgeCount: val}) }} />

          <Label>가중치 범위</Label>
          {config.weightRange.map((v, idx) => (
            <div key={`weight-range-${idx}`}>
              <VariableInput key={`weight-range-${idx}-1`} blockIndex={blockIndex} variableIndex={10} initValue={v.min} onChange={(val) => updateWeightRange(idx, { ...v, min: val })} />
              <VariableInput key={`weight-range-${idx}-2`} blockIndex={blockIndex} variableIndex={10} initValue={v.max} onChange={(val) => updateWeightRange(idx, { ...v, max: val })} />
            </div>
          ))}
          <Button onClick={addWeightRange}>수 범위 추가</Button>

          <Checkbox checked={config.isPerfect} id={'is-perfect'} onCheckedChange={(chk) => { updateConfig({...config, isPerfect: !!chk.valueOf() }) }}/> <Label htmlFor={'is-perfect'}>완전그래프 여부</Label>
          <Checkbox checked={config.isConnect} id={'is-connect'} onCheckedChange={(chk) => { updateConfig({...config, isConnect: !!chk.valueOf() }) }}/> <Label htmlFor={'is-connect'}>연결그래프 여부</Label>
          <Checkbox checked={config.isCycle} id={'is-cycle'} onCheckedChange={(chk) => { updateConfig({...config, isCycle: !!chk.valueOf() }) }}/> <Label htmlFor={'is-cycle'}>사이클 여부</Label>
        </Card>
        <Card>
          <Output blockIndex={blockIndex} />
        </Card>
      </Card>
    </div>
  )
}

export default GraphBlock;
