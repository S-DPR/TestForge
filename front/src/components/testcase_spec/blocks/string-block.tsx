import {Card} from "@/components/ui/card";
import {Label} from "@/components/ui/label";
import {Button} from "@/components/ui/button";
import Variable from "@/components/testcase_spec/variable";
import VariableInput from "@/components/testcase_spec/variable-input";
import React, {useContext} from "react";
import {TestcaseContext} from "@/context/TestcaseContext";
import Output from "@/components/testcase_spec/output";
import {Range} from "@/components/testcase_spec/define-range";
import {Checkbox} from "@/components/ui/checkbox";
import {MatrixConfig} from "@/components/testcase_spec/blocks/matrix-block";

interface StringBlockProps {
  blockIndex: number;
}

const StringBlock = ({ blockIndex }: StringBlockProps) => {
  const ctx = useContext(TestcaseContext);
  if (!ctx) throw new Error('근데 이거 계속 반복되네');

  const { blocks, setBlocks, addVariable, updateBlockRepeat } = ctx;
  const currentBlock = blocks[blockIndex]
  const currentVariable = currentBlock.variables;
  const config: MatrixConfig = blocks[blockIndex].config as MatrixConfig;

  const updateConfig = (config: MatrixConfig) => {
    setBlocks((prev) => {
      const newBlocks = structuredClone(prev);
      newBlocks[blockIndex].config = config;
      return newBlocks;
    })
  }

  const updateNumRange = (weightRangeIndex: number, range: Range) => {
    setBlocks((prev) => {
      const newBlocks = structuredClone(prev);
      const cfg: MatrixConfig = newBlocks[blockIndex].config as MatrixConfig;
      cfg.numRange[weightRangeIndex] = range;
      return newBlocks;
    })
  }

  const addNumRange = () => {
    setBlocks((prev) => {
      const newBlocks = structuredClone(prev);
      const cfg: MatrixConfig = newBlocks[blockIndex].config as MatrixConfig;
      cfg.numRange.push({ min: '0', max: '0' });
      return newBlocks;
    })
  }

  config.numType = 'char';

  return (
    <Card className="p-6 space-y-6 bg-white border border-gray-200 rounded-lg shadow-sm">
      {/* 반복 횟수 */}
      <div className="space-y-1">
        <Label className="text-sm text-gray-700">반복 횟수</Label>
        <VariableInput
          value={currentBlock.repeat}
          onChange={(val) => updateBlockRepeat(blockIndex, val)}
          showChar={false}
          blockIndex={blockIndex - 1}
          variableIndex={10}
        />
      </div>

      {/* 변수 설정 */}
      <div className="space-y-2">
        <Label className="text-sm text-gray-700">변수 설정</Label>
        <div className="space-y-2">
          {currentVariable.map((v, idx) =>
              !v.isReserved && (
                <Variable
                  key={idx}
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
              ranges: [],
              isReserved: false,
            })
          }
        >
          변수 추가
        </Button>
      </div>

      {/* 상세 설정 */}
      <div className="space-y-4">
        <Label className="text-sm text-gray-700">상세 설정</Label>

        <div className="space-y-1">
          <Label className="text-sm text-gray-600">문자열 길이</Label>
          <VariableInput
            value={config.colSize}
            blockIndex={blockIndex}
            showChar={false}
            variableIndex={10}
            onChange={(val) => updateConfig({ ...config, colSize: val })}
          />
        </div>

        {/*<div className="space-y-1">*/}
        {/*  <Label className="text-sm text-gray-600">세로 길이</Label>*/}
        {/*  <VariableInput*/}
        {/*    value={"1"}*/}
        {/*    blockIndex={blockIndex}*/}
        {/*    showChar={false}*/}
        {/*    variableIndex={10}*/}
        {/*    onChange={(val) => updateConfig({ ...config, rowSize: val })}*/}
        {/*  />*/}
        {/*</div>*/}

        {/*<div className="space-y-1">*/}
        {/*  <Label className="text-sm text-gray-600">내부 타입</Label>*/}
        {/*</div>*/}

        <div className="space-y-2">
          <Label className="text-sm text-gray-600">아스키코드 범위</Label>
          <div className="space-y-2">
            {config.numRange.map((v, idx) => (
              <div key={idx} className="flex gap-2">
                <VariableInput
                  blockIndex={blockIndex}
                  variableIndex={10}
                  showChar={false}
                  value={v.min}
                  onChange={(val) =>
                    updateNumRange(idx, { ...v, min: val })
                  }
                />
                <VariableInput
                  blockIndex={blockIndex}
                  variableIndex={10}
                  showChar={false}
                  value={v.max}
                  onChange={(val) =>
                    updateNumRange(idx, { ...v, max: val })
                  }
                />
              </div>
            ))}
          </div>
          <Button size="sm" onClick={addNumRange}>
            아스키코드 범위 추가
          </Button>
        </div>

        {/* 체크박스 그룹 */}
        <div className="space-y-2">
          {[
            ["isDistinct", "중복 없는 행렬"],
            ["randomEmpty", "랜덤한 위치 비우기"],
          ].map(([key, label]) => (
            <div key={key} className="flex items-center gap-2">
              <Checkbox
                checked={(config as any)[key]}
                id={key}
                onCheckedChange={(chk) =>
                  updateConfig({ ...config, [key]: !!chk.valueOf() })
                }
              />
              <Label htmlFor={key}>{label}</Label>
            </div>
          ))}
        </div>
      </div>

      {/* Output */}
      <div>
        <Label className="text-sm text-gray-700">출력 설정</Label>
        <Output blockIndex={blockIndex} defaultSeparator={""} />
      </div>
    </Card>
  )
}

export default StringBlock;
