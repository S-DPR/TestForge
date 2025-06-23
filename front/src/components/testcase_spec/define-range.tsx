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
    minValue: string;
    maxValue: string;
    onMinChange: (value: string) => void;
    onMaxChange: (value: string) => void;
    onDeleteClick: () => void;
}

const DefineRange = ({ blockIndex, variableIndex, minValue, maxValue, onMinChange, onMaxChange, onDeleteClick }: DefineRangeSpec) => {
  const ctx = useContext(TestcaseContext);
  if (!ctx) throw new Error("context 없음. 개판임.");

  return (
    <div className="flex justify-center items-center gap-2 w-full">
      <VariableInput
        blockIndex={blockIndex}
        variableIndex={variableIndex}
        value={minValue}
        showChar={false}
        onChange={(val) => onMinChange(val)}
      />
      <span className="text-gray-500 text-sm"> to </span>
      <VariableInput
        blockIndex={blockIndex}
        variableIndex={variableIndex}
        value={maxValue}
        showChar={false}
        onChange={(val) => onMaxChange(val)}
      />
      <a onClick={onDeleteClick} style={{ cursor: 'pointer' }}>
        ❌
      </a>
    </div>
  );
}

export default DefineRange
