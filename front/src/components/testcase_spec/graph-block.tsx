import {Card} from "@/components/ui/card";
import {Label} from "@/components/ui/label";
import {Button} from "@/components/ui/button";
import Variable from "@/components/testcase_spec/variable";
import VariableInput from "@/components/testcase_spec/variable-input";
import {useContext} from "react";
import {AbstractConfig, TestcaseContext} from "@/context/TestcaseContext";
import Output from "@/components/testcase_spec/output";
import {Range} from "@/components/testcase_spec/define-range";
import {Checkbox} from "@/components/ui/checkbox";

export interface GraphConfig extends AbstractConfig {
  nodeCount: string;
  edgeCount: string;
  weightRange: Range[];
  isPerfect: boolean;
  isConnect: boolean;
  isCycle: boolean;
}

interface GraphBlockProps {
  blockIndex: number;
}

const GraphBlock = ({ blockIndex }: GraphBlockProps) => {
  const ctx = useContext(TestcaseContext);
  if (!ctx) throw new Error('근데 이거 계속 반복되네');

  const { blocks, addVariable } = ctx;
  const currentVariable = blocks[blockIndex].variables;

  return (
    <div>
      <Card>
        <Card>
          <Label>반복 횟수</Label>
          <VariableInput blockIndex={blockIndex-1} variableIndex={10}></VariableInput>
        </Card>
        <Card>
          <Label>변수 설정</Label>
          {currentVariable.map((v, idx) => !v.isReserved && (
            <Variable
              key={idx}
              blockIndex={blockIndex}
              variableIndex={idx}
            />
          ))}
          <Button onClick={() => addVariable(blockIndex, {name: '', type: '', ranges: [], isReserved: false})}>변수 추가</Button>
        </Card>
        <Card>
          <Label>상세 설정</Label>

          <Label>노드 개수</Label>
          <VariableInput blockIndex={blockIndex} variableIndex={10}></VariableInput>

          <Label>간선 개수</Label>
          <VariableInput blockIndex={blockIndex} variableIndex={10}></VariableInput>

          <Label>가중치 범위</Label>
          <VariableInput blockIndex={blockIndex} variableIndex={10}></VariableInput>
          <VariableInput blockIndex={blockIndex} variableIndex={10}></VariableInput>

          <Checkbox id={'is-perfect'}/> <Label htmlFor={'is-perfect'}>완전그래프 여부</Label>
          <Checkbox id={'is-connect'}/> <Label htmlFor={'is-connect'}>연결그래프 여부</Label>
          <Checkbox id={'is-cycle'}/> <Label htmlFor={'is-cycle'}>사이클 여부</Label>
        </Card>
        <Card>
          <Output blockIndex={blockIndex} />
        </Card>
      </Card>
    </div>
  )
}

export default GraphBlock;
