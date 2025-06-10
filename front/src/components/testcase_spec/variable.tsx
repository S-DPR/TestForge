import DefineRange, {Range} from "@/components/testcase_spec/define-range";
import {Label} from "@/components/ui/label";
import {Input} from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectTrigger,
  SelectValue
} from "@/components/ui/select";
import React from "react";
import {Button} from "@/components/ui/button";


export interface VariableSpec {
  name: string;
  type: string;
  ranges: Range[];
}

export interface VariableProps {
  variable: VariableSpec[][];
  blockIndex: number;
  variableIndex: number;
  onVariableRangeAddClick: (blockIndex: number, variableIndex: number) => void;
  onRemove: (blockIndex: number, variableIndex: number) => void;
  onChange: (field: string, value: string) => void;
  updateVariablesRange: (blockIndex: number, variableIndex: number, rangeIndex: number, field: string, value: string) => void;
}

const Variable = ({ variable, blockIndex, variableIndex, onRemove, onChange, onVariableRangeAddClick, updateVariablesRange }: VariableProps) => {
  const currentVar = variable[blockIndex][variableIndex];
  return (
    <div>
      <Label>변수 이름</Label>
      <Input defaultValue={currentVar.name} onChange={(e) => onChange('name', e.target.value)} ></Input>

      <Label>변수 타입</Label>
      <Select value={currentVar.type} onValueChange={(e) => onChange('type', e)}>
        <SelectTrigger className="w-[180px] border-gray-600 rounded-md px-3 py-2">
          <SelectValue placeholder="변수 타입" />
        </SelectTrigger>
        <SelectContent className="bg-white border border-gray-700">
          <SelectGroup>
            <SelectItem value="Number">Number</SelectItem>
            <SelectItem value="Char">Char</SelectItem>
            <SelectItem value="Enum">Enum</SelectItem>
          </SelectGroup>
        </SelectContent>
      </Select>

      <Label>범위</Label>
      {currentVar.ranges.map((r, i) => (
          <DefineRange key={i} variable={variable} blockIndex={blockIndex} variableIndex={variableIndex} rangeIndex={i} updateVariablesRange={updateVariablesRange}/>
      ))}
      <Button onClick={() => onVariableRangeAddClick(blockIndex, variableIndex)}>범위 추가</Button>

      <Button onClick={() => onRemove(blockIndex, variableIndex)}>변수 제거</Button>
    </div>
  )
}

export default Variable;
