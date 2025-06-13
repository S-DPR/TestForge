import VariableInput from "@/components/testcase_spec/variable-input";
import { Label } from "@/components/ui/label";
import { TestcaseContext } from "@/context/TestcaseContext";
import {useContext, useState} from "react";
import { Button } from "@/components/ui/button";

export type OutputType = {
  sequence: string[];
  separator: string;
}

interface OutputSpec {
  blockIndex: number;
};

const Output = ({ blockIndex }: OutputSpec) => {
  const ctx = useContext(TestcaseContext);
  if (!ctx) throw new Error("또 콘텍스트야");

  const {
    blocks,
    updateOutputSequence,
    removeOutputSequence,
    updateSeparator,
  } = ctx;

  const output = blocks[blockIndex].output;
  const [inputValue, setInputValue] = useState("");
  const [separator, setSeparator] = useState(output.separator);

  const handleAdd = () => {
    if (inputValue.trim() === "") return;
    const newSequence = [...output.sequence, inputValue];
    updateOutputSequence(blockIndex, -1, newSequence); // -1이면 전체 치환
    setInputValue("");
  };

  return (
    <div className="space-y-6 border border-gray-200 rounded-md p-6">
      {/* 출력값 목록 */}
      <div className="space-y-1">
        <Label className="text-sm text-gray-700 block">출력값 목록</Label>
        <div className="flex flex-wrap gap-2">
          {output.sequence.map((item, idx) => (
            <Button
              key={idx}
              variant="secondary"
              size="sm"
              className="rounded-full text-xs px-3 py-1"
              onClick={() => removeOutputSequence(blockIndex, idx)}
            >
              {item} ✕
            </Button>
          ))}
        </div>
      </div>

      {/* 출력값 입력 */}
      <div className="space-y-1">
        <Label className="text-sm text-gray-700 block">출력값 입력</Label>
        <div className="flex gap-2">
          <VariableInput
            value={inputValue}
            onChange={(val) => {
              setInputValue(val)
            }}
            isRenderReserved={true}
            showChar={true}
            blockIndex={blockIndex}
            variableIndex={10}
          />
          <Button onClick={handleAdd}>추가</Button>
        </div>
      </div>

      {/* 구분자 설정 */}
      <div className="space-y-1">
        <Label className="text-sm text-gray-700 block">구분자 설정</Label>
        <VariableInput
          value={separator}
          onChange={(val) => {
            setSeparator(val)
            updateSeparator(blockIndex, val)
          }}
          showChar={true}
          blockIndex={blockIndex}
          variableIndex={10}
        />
      </div>
    </div>
  );
};

export default Output;
