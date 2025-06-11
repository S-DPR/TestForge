import {Card} from "@/components/ui/card";
import {Label} from "@/components/ui/label";
import {Button} from "@/components/ui/button";
import Variable, {VariableSpec} from "@/components/testcase_spec/variable";
import VariableInput from "@/components/testcase_spec/variable-input";
import {useContext} from "react";
import {TestcaseContext} from "@/context/TestcaseContext";
import Output from "@/components/testcase_spec/output";

interface LineBlockProps {
  blockIndex: number;
}

const LineBlock = ({ blockIndex }: LineBlockProps) => {
  const ctx = useContext(TestcaseContext);
  if (!ctx) throw new Error('근데 이거 계속 반복되네');

  const { variables, addVariable } = ctx;

  return (
    <div>
      <Card>
        <Card>
          <Label>반복 횟수</Label>
          <VariableInput blockIndex={blockIndex-1} variableIndex={999}></VariableInput>
        </Card>
        <Card>
          <Label>변수 설정</Label>
          {variables[blockIndex].map((v, idx) => (
                <Variable
                    key={idx}
                    blockIndex={blockIndex}
                    variableIndex={idx}
                />
          ))}
          <Button onClick={() => addVariable(blockIndex)}>변수 추가</Button>
        </Card>
        <Card>
          <Output blockIndex={blockIndex} />
        </Card>
      </Card>
    </div>
  )
}

export default LineBlock;
