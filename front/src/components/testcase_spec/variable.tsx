import DefineRange from "@/components/testcase_spec/define-range";
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
  ranges: (number[] | string[])[];
}

export interface VariableProps {
  blockIndex: number;
  variableIndex: number;
  onRemove: (blockIndex: number, variableIndex: number) => void;
}

const Variable = ({ blockIndex, variableIndex, onRemove }: VariableProps) => {
  console.log(`나는 ${blockIndex}번째 블럭의 ${variableIndex}번째 변수`);
  return (
    <div>
      <Label>변수 이름</Label>
      <Input></Input>

      <Label>변수 타입</Label>
      <Select>
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
      <DefineRange></DefineRange>

      <Button onClick={() => onRemove(blockIndex, variableIndex)}>변수 제거</Button>
    </div>
  )
}

export default Variable;
