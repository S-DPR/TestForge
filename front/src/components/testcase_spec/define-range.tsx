import {Input} from "@/components/ui/input";
import React from "react";

export type Range = {
    min: string;
    max: string;
}

interface DefineRangeSpec {
    blockIndex: number;
    variableIndex: number;
    rangeIndex: number;
    min: string;
    max: string;
    updateVariablesRange: (blockIndex: number, variableIndex: number, rangeIndex: number, field: string, value: string) => void;
}

const DefineRange = ({ min, max }: DefineRangeSpec) => {
  return (
    <div>
      <Input placeholder={"min"} defaultValue={min}></Input>
      <Input placeholder={"max"} defaultValue={max}></Input>
    </div>
  )
}

export default DefineRange
