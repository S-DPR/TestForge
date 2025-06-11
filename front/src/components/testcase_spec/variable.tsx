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
import React, {useContext} from "react";
import {Button} from "@/components/ui/button";
import {TestcaseContext} from "@/context/TestcaseContext";


export interface VariableSpec {
  name: string;
  type: string;
  ranges: Range[];
  isReserved: boolean;
}

export interface VariableProps {
  blockIndex: number;
  variableIndex: number;
}

const Variable = ({ blockIndex, variableIndex }: VariableProps) => {
  const context = useContext(TestcaseContext);
  if (!context) throw new Error("context 없음. 개판임");

  const { blocks, updateVariable, addVariableRange, removeVariable } = context;
  const currentVariable = blocks[blockIndex].variables[variableIndex];

  return (
    <div>
      <Label>변수 이름</Label>
      <Input defaultValue={currentVariable.name} onChange={(e) => updateVariable(blockIndex, variableIndex, { ...currentVariable, name: e.target.value })} ></Input>

      <Label>변수 타입</Label>
      <Select value={currentVariable.type} onValueChange={(val) => updateVariable(blockIndex, variableIndex, { ...currentVariable, type: val })}>
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
      {currentVariable.ranges.map((r, i) => (
          <DefineRange key={i} blockIndex={blockIndex} variableIndex={variableIndex} rangeIndex={i} />
      ))}
      <Button onClick={() => addVariableRange(blockIndex, variableIndex, { min: '0', max: '0' })}>범위 추가</Button>

      <Button onClick={() => removeVariable(blockIndex, variableIndex)}>변수 제거</Button>
    </div>
  )
}

export default Variable;
