import {Card} from "@/components/ui/card";
import {Label} from "@/components/ui/label";
import {Button} from "@/components/ui/button";
import Variable from "@/components/testcase_spec/variable";
import VariableInput from "@/components/testcase_spec/variable-input";
import React, {useContext, useState} from "react";
import {AbstractConfig, TestcaseContext} from "@/context/TestcaseContext";
import Output from "@/components/testcase_spec/output";
import {Range} from "@/components/testcase_spec/define-range";
import {Checkbox} from "@/components/ui/checkbox";
import {Select, SelectContent, SelectGroup, SelectItem, SelectTrigger, SelectValue} from "@/components/ui/select";

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

const GraphBlock = ({ blockIndex }: MatrixBlockProps) => {
  const ctx = useContext(TestcaseContext);
  if (!ctx) throw new Error('근데 이거 계속 반복되네');

  const { blocks, setBlocks, addVariable, updateBlockRepeat } = ctx;
  const currentBlock = blocks[blockIndex]
  const currentVariable = currentBlock.variables;
  const config: MatrixConfig = blocks[blockIndex].config as MatrixConfig;

  const updateConfig = (config: MatrixConfig) => {
    setBlocks((prev) => {
      const newBlocks = structuredClone(prev);
      newBlocks[blockIndex].config = config;
      console.log(newBlocks[blockIndex].config);
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

  return (
    <div>
      <Card>
        <Card>
          <Label>반복 횟수</Label>
          <VariableInput initValue={currentBlock.repeat} onChange={(val) => updateBlockRepeat(blockIndex, val)} blockIndex={blockIndex-1} variableIndex={10}></VariableInput>
        </Card>
        <Card>
          <Label>변수 설정</Label>
          {currentVariable.map((v, idx) => !v.isReserved && (
            <Variable
              key={idx}
              blockIndex={blockIndex}
              variableIndex={idx}
            />
          ))}
          <Button onClick={() => addVariable(blockIndex, {name: '', type: '', ranges: [], isReserved: false})}>변수 추가</Button>
        </Card>
        <Card>
          <Label>상세 설정</Label>

          <Label>가로 길이</Label>
          <VariableInput initValue={config.colSize} blockIndex={blockIndex} variableIndex={10} onChange={(val) => { updateConfig({...config, colSize: val}) }} />

          <Label>세로 길이</Label>
          <VariableInput initValue={config.rowSize} blockIndex={blockIndex} variableIndex={10} onChange={(val) => { updateConfig({...config, rowSize: val}) }} />

          <Label>내부 타입</Label>
          <Select value={config.numType} onValueChange={(val) => updateConfig({ ...config, numType: val })}>
            <SelectTrigger className="w-[180px] border-gray-600 rounded-md px-3 py-2">
              <SelectValue placeholder="변수 타입" />
            </SelectTrigger>
            <SelectContent className="bg-white border border-gray-700">
              <SelectGroup>
                <SelectItem value="int">Number</SelectItem>
                <SelectItem value="char">Char</SelectItem>
                <SelectItem value="enum">Enum</SelectItem>
              </SelectGroup>
            </SelectContent>
          </Select>

          <Label>수 범위</Label>
          {config.numRange.map((v, idx) => (
            <>
              <VariableInput blockIndex={blockIndex} variableIndex={10} initValue={v.min} onChange={(val) => updateNumRange(idx, { ...v, min: val })} />
              <VariableInput blockIndex={blockIndex} variableIndex={10} initValue={v.max} onChange={(val) => updateNumRange(idx, { ...v, max: val })} />
            </>
          ))}
          <Button onClick={addNumRange}>수 범위 추가</Button>

          <Checkbox checked={config.isDistinct} id={'is-distinct'} onCheckedChange={(chk) => { updateConfig({...config, isDistinct: !!chk.valueOf() }) }}/> <Label htmlFor={'is-distinct'}>중복 없는 행렬</Label>
          <Checkbox checked={config.randomEmpty} id={'random-empty'} onCheckedChange={(chk) => { updateConfig({...config, randomEmpty: !!chk.valueOf() }) }}/> <Label htmlFor={'random-empty'}>랜덤한 위치 비우기</Label>
          <Checkbox checked={config.isGraph} id={'is-graph'} onCheckedChange={(chk) => { updateConfig({...config, isGraph: !!chk.valueOf() }) }}/> <Label htmlFor={'is-graph'}>행렬그래프 여부</Label>
          <Checkbox checked={config.isSymmetric} id={'is-symmetric'} onCheckedChange={(chk) => { updateConfig({...config, isSymmetric: !!chk.valueOf() }) }}/> <Label htmlFor={'is-symmetric'}>대칭행렬 여부</Label>
        </Card>
        <Card>
          <Output blockIndex={blockIndex} />
        </Card>
      </Card>
    </div>
  )
}

export default GraphBlock;
