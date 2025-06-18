import {Label} from "@/components/ui/label";
import Variable from "@/components/testcase_spec/variable";
import {Button} from "@/components/ui/button";
import React, {useContext} from "react";
import {TestcaseContext} from "@/context/TestcaseContext";

const SettingVariable = ({ blockIndex }: { blockIndex: number }) => {
  const ctx = useContext(TestcaseContext);
  if (!ctx) throw new Error('근데 이거 계속 반복되네');

  const { blocks, addVariable } = ctx;
  const currentBlock = blocks[blockIndex]
  const currentVariable = currentBlock.variable;

  return (<div className="space-y-2">
    <div className="space-y-2">
      {currentVariable.map((v, idx) =>
          !v.isReserved && (
            <Variable
              key={`${blockIndex}-variable-${idx}`}
              blockIndex={blockIndex}
              variableIndex={idx}
            />
          )
      )}
    </div>
    <Button
      size="sm"
      variant="outline"
      onClick={() =>
        addVariable(blockIndex, {
          name: "",
          type: "",
          range: [],
          isReserved: false,
        })
      }
    >
      변수 추가
    </Button>
  </div>)
}

export default SettingVariable;
