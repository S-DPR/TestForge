import {Card} from "@/components/ui/card";
import {Label} from "@/components/ui/label";
import {Button} from "@/components/ui/button";
import {Input} from "@/components/ui/input";
import Variable, {VariableSpec} from "@/components/testcase_spec/variable";

interface LineBlockProps {
  blockIndex: number;
  variables: VariableSpec[];
  onVariableAddClick: (blockIndex: number) => void;
  onRemoveVariable: (blockIndex: number, variableIndex: number) => void;
}

const LineBlock = ({ blockIndex, variables, onVariableAddClick, onRemoveVariable }: LineBlockProps) => {
  return (
    <div>
      <Card>
        <Card>
          <Label>반복 횟수</Label>
          <Input defaultValue={"[여긴 추후 수정, select로 선택 혹은 input으로 임력]"}></Input>
        </Card>
        <Card>
          <Label>변수 설정</Label>
          {variables.map((v, idx) => (
                <Variable
                    variable={v}
                    key={idx}
                    blockIndex={blockIndex}
                    variableIndex={idx}
                    onRemove={() => onRemoveVariable(blockIndex, idx)}
                    onChange={() => {
                    }}
                />
          ))}
          <Button onClick={() => onVariableAddClick(blockIndex)}>변수 추가</Button>
        </Card>
        <Card>
          <Input defaultValue={"[여긴 sequence 및 separator 설정하는 부분, 변수는 반복횟수처럼 해둬야할거고..]"}></Input>
        </Card>
      </Card>
    </div>
  )
}

export default LineBlock;
