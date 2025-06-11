import {Card} from "@/components/ui/card";
import {Label} from "@/components/ui/label";
import {Button} from "@/components/ui/button";
import Variable from "@/components/testcase_spec/variable";
import VariableInput from "@/components/testcase_spec/variable-input";
import {useContext} from "react";
import {AbstractConfig, TestcaseContext} from "@/context/TestcaseContext";
import Output from "@/components/testcase_spec/output";

export interface LineConfig extends AbstractConfig {
  _: null;
}

interface LineBlockProps {
  blockIndex: number;
}

const LineBlock = ({ blockIndex }: LineBlockProps) => {
  const ctx = useContext(TestcaseContext);
  if (!ctx) throw new Error('근데 이거 계속 반복되네');

  const { blocks, addVariable, updateBlockRepeat } = ctx;
  const currentBlock = blocks[blockIndex]
  const currentVariable = currentBlock.variables;

  return (
    <Card className="p-6 space-y-6 bg-white border border-gray-200 shadow-sm rounded-lg">
      {/* 반복 횟수 */}
      <div className="space-y-2">
        <Label className="text-sm text-gray-700">반복 횟수</Label>
        <VariableInput
          value={currentBlock.repeat}
          onChange={(val) => updateBlockRepeat(blockIndex, val)}
          blockIndex={blockIndex - 1}
          variableIndex={999}
        />
      </div>

      {/* 변수 설정 */}
      <div className="space-y-3">
        <Label className="text-sm text-gray-700">변수 설정</Label>
        <div className="space-y-2">
          {currentVariable
            .filter((v) => !v.isReserved)
            .map((v, idx) => (
              <Variable
                key={idx}
                blockIndex={blockIndex}
                variableIndex={idx}
              />
            ))}
        </div>
        <Button
          variant="outline"
          size="sm"
          onClick={() =>
            addVariable(blockIndex, {
              name: "",
              type: "",
              ranges: [],
              isReserved: false,
            })
          }
        >
          변수 추가
        </Button>
      </div>

      {/* Output */}
      <div>
        <Label className="text-sm text-gray-700">출력 설정</Label>
        <Output blockIndex={blockIndex} />
      </div>
    </Card>

  )
}

export default LineBlock;
