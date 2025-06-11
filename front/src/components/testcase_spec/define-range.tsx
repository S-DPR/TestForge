import React, {useContext} from "react";
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

  const { blocks, updateVariableRange } = ctx;
  console.log(blocks)
  const currentRange = blocks[blockIndex].variables[variableIndex].ranges[rangeIndex];

  return (
    <div>
      <VariableInput blockIndex={blockIndex} variableIndex={variableIndex} onChange={(val) => updateVariableRange(blockIndex, variableIndex, rangeIndex, { ...currentRange, min: val })} />
      <VariableInput blockIndex={blockIndex} variableIndex={variableIndex} onChange={(val) => updateVariableRange(blockIndex, variableIndex, rangeIndex, { ...currentRange, max: val })} />
    </div>
  )
}

export default DefineRange
