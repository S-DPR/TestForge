import React, {useContext} from "react";
import {VariableSpec} from "@/components/testcase_spec/variable";
import VariableInput from "@/components/testcase_spec/variable-input";
import {TestcaseContext} from "@/context/TestcaseContext";

export type Range = {
    min: string;
    max: string;
}

interface DefineRangeSpec {
    blockIndex: number;
    variableIndex: number;
    rangeIndex: number;
}

// 이거 VariableInput으로 바꿔야함
const DefineRange = ({ blockIndex, variableIndex, rangeIndex }: DefineRangeSpec) => {
  const ctx = useContext(TestcaseContext);
  if (!ctx) throw new Error("context 없음. 개판임.");

  const { updateVariablesRange } = ctx;

  return (
    <div>
      <VariableInput blockIndex={blockIndex} variableIndex={variableIndex} onChange={(val) => updateVariablesRange(blockIndex, variableIndex, rangeIndex, 'min', val)} />
      <VariableInput blockIndex={blockIndex} variableIndex={variableIndex} onChange={(val) => updateVariablesRange(blockIndex, variableIndex, rangeIndex, 'max', val)} />
    </div>
  )
}

export default DefineRange
