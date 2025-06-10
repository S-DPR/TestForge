import React from "react";
import {VariableSpec} from "@/components/testcase_spec/variable";
import VariableInput from "@/components/testcase_spec/variable-input";

export type Range = {
    min: string;
    max: string;
}

interface DefineRangeSpec {
    variable: VariableSpec[][];
    blockIndex: number;
    variableIndex: number;
    rangeIndex: number;
    updateVariablesRange: (blockIndex: number, variableIndex: number, rangeIndex: number, field: string, value: string) => void;
}

// 이거 VariableInput으로 바꿔야함
const DefineRange = ({ variable, blockIndex, variableIndex, rangeIndex, updateVariablesRange }: DefineRangeSpec) => {
  return (
    <div>
      <VariableInput variable={variable} blockIndex={blockIndex} variableIndex={variableIndex} onChange={(val) => updateVariablesRange(blockIndex, variableIndex, rangeIndex, 'min', val)} />
      <VariableInput variable={variable} blockIndex={blockIndex} variableIndex={variableIndex} onChange={(val) => updateVariablesRange(blockIndex, variableIndex, rangeIndex, 'max', val)} />
    </div>
  )
}

export default DefineRange
