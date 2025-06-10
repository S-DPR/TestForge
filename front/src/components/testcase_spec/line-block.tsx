import {Card} from "@/components/ui/card";
import {Label} from "@/components/ui/label";
import {Button} from "@/components/ui/button";
import Variable, {VariableSpec} from "@/components/testcase_spec/variable";
import VariableInput from "@/components/testcase_spec/variable-input";

interface LineBlockProps {
  blockIndex: number;
  variables: VariableSpec[][];
  onVariableAddClick: (blockIndex: number) => void;
  onVariableRangeAddClick: (blockIndex: number, variableIndex: number) => void;
  onRemoveVariable: (blockIndex: number, variableIndex: number) => void;
  updateVariables: (blockIndex: number, variableIndex: number, field: string, value: string) => void;
  updateVariablesRange: (blockIndex: number, variableIndex: number, rangeIndex: number, field: string, value: string) => void;
}

const LineBlock = ({ blockIndex, variables, onVariableAddClick, onRemoveVariable, updateVariables, updateVariablesRange, onVariableRangeAddClick }: LineBlockProps) => {
  return (
    <div>
      <Card>
        <Card>
          <Label>반복 횟수</Label>
          <VariableInput variable={variables} blockIndex={blockIndex-1} variableIndex={999}></VariableInput>
        </Card>
        <Card>
          <Label>변수 설정</Label>
          {variables[blockIndex].map((v, idx) => (
                <Variable
                    key={idx}
                    variable={variables}
                    blockIndex={blockIndex}
                    variableIndex={idx}
                    onRemove={() => onRemoveVariable(blockIndex, idx)}
                    onChange={(field, value) => updateVariables(blockIndex, idx, field, value)}
                    onVariableRangeAddClick={onVariableRangeAddClick}
                    updateVariablesRange={updateVariablesRange}
                />
          ))}
          <Button onClick={() => onVariableAddClick(blockIndex)}>변수 추가</Button>
        </Card>
        <Card>
          <VariableInput variable={variables} blockIndex={blockIndex} variableIndex={999}></VariableInput>
        </Card>
      </Card>
    </div>
  )
}

export default LineBlock;
