import VariableInput from "@/components/testcase_spec/variable-input";
import {Label} from "@/components/ui/label";
import {TestcaseContext} from "@/context/TestcaseContext";
import {useContext} from "react";
import {Button} from "@/components/ui/button";

type Output = {
  sequence: string[];
  separator: string;
}

interface OutputSpec {
  blockIndex: number;
}

const Output = ({ blockIndex }: OutputSpec) => {
  const ctx = useContext(TestcaseContext);
  if (!ctx) throw new Error("또 콘텍스트야");

  const { blocks, addOutputSequence, updateOutputSequence } = ctx;

  return (
    <>
      {blocks[blockIndex].output.sequence.map((seq, idx) => (
        <VariableInput
          key={idx}
          blockIndex={blockIndex}
          variableIndex={999}
          initValue={seq}
          onChange={(val) => updateOutputSequence(blockIndex, idx, val)}
          isRenderReserved={true}
        />
      ))}
      <Button onClick={() => addOutputSequence(blockIndex)}>sequence 추가</Button>

      <Label>구분자 설정</Label>
      <VariableInput blockIndex={blockIndex} variableIndex={999} />
    </>
  )
}

export default Output;
