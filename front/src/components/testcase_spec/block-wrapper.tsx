import {Card, CardContent, CardHeader} from "@/components/ui/card";
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue
} from "@/components/ui/select";
import React, {ReactNode, useContext} from "react";
import {TestcaseContext} from "@/context/TestcaseContext";
import {Button} from "@/components/ui/button";
import {Accordion, AccordionContent, AccordionItem, AccordionTrigger} from "@/components/ui/accordion";
import SettingVariable from "@/components/testcase_spec/setting-variable";
import Output from "@/components/testcase_spec/output";
import {Label} from "@/components/ui/label";
import VariableInput from "@/components/testcase_spec/variable-input";

interface BlockWrapperProps {
  blockIndex: number;
  defaultSetting?: React.ReactNode;
  specialSetting?: React.ReactNode;
  isRenderOutput : boolean;
}

const BlockWrapper = ({ blockIndex, defaultSetting, specialSetting, isRenderOutput }: BlockWrapperProps) => {
  const ctx = useContext(TestcaseContext);
  if (!ctx) throw new Error('콘텍스트없서요');

  const { blocks, updateBlockType, deleteBlockType, updateBlockRepeat } = ctx;
  const currentBlock = blocks[blockIndex]

  return (
    <Card className="bg-white shadow-sm border border-gray-200 rounded-xl p-4">
      <CardHeader className="pb-2 flex flex-row justify-between items-center">
        <Select value={blocks[blockIndex]?.visibleType ?? 'line'} onValueChange={(type: string) => updateBlockType(blockIndex, type)}>
          <SelectTrigger className="w-[180px] border-gray-300 rounded-md px-3 py-2 text-sm focus:ring-2 focus:ring-primary focus:outline-none">
            <SelectValue placeholder="블럭 타입 선택" />
          </SelectTrigger>
          <SelectContent className="bg-white border border-gray-200 shadow-md rounded-md">
            <SelectGroup>
              <SelectLabel>타입</SelectLabel>
              <SelectItem value="Line">Line</SelectItem>
              <SelectItem value="Graph">Graph</SelectItem>
              <SelectItem value="Matrix">Matrix</SelectItem>
              <SelectItem value="String">String</SelectItem>
            </SelectGroup>
          </SelectContent>
        </Select>
      </CardHeader>
      <CardContent className="pt-4">
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

        <Accordion
          type="single"
          collapsible
          className="w-full"
        >
          <AccordionItem value={"variables"}>
            <AccordionTrigger>변수 설정</AccordionTrigger>
            <AccordionContent>
              <SettingVariable blockIndex={blockIndex} />
            </AccordionContent>
          </AccordionItem>
          {defaultSetting && <AccordionItem value={"default-setting"}>
              <AccordionTrigger>기본 설정</AccordionTrigger>
              <AccordionContent>
                {defaultSetting}
              </AccordionContent>
          </AccordionItem>}
          {specialSetting && <AccordionItem value={"special-setting"}>
              <AccordionTrigger>특수 설정</AccordionTrigger>
              <AccordionContent>
                {specialSetting}
              </AccordionContent>
          </AccordionItem>}
          {isRenderOutput && <AccordionItem value={"output"}>
            <AccordionTrigger>출력 설정</AccordionTrigger>
            <AccordionContent>
              <Output blockIndex={blockIndex} />
            </AccordionContent>
          </AccordionItem>}
        </Accordion>
      </CardContent>
      <Button className="bg-red-600 hover:bg-red-700 text-white" onClick={() => {deleteBlockType(blockIndex)}}>블럭 삭제</Button>
    </Card>
  )
}

export default BlockWrapper;
