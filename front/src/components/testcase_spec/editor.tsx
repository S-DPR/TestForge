import React, {ReactNode, useContext} from "react";
import {BlockSpec, TestcaseContext} from "@/context/TestcaseContext";
import LineBlock from "@/components/testcase_spec/blocks/line-block";
import GraphBlock from "@/components/testcase_spec/blocks/graph-block";
import MatrixBlock from "@/components/testcase_spec/blocks/matrix-block";
import {Button} from "@/components/ui/button";
import {Card, CardContent, CardDescription, CardHeader, CardTitle} from "@/components/ui/card";
import StringBlock from "@/components/testcase_spec/blocks/string-block";
import {Accordion, AccordionContent, AccordionItem, AccordionTrigger} from "@/components/ui/accordion";
import {HoverCard, HoverCardContent, HoverCardTrigger} from "@/components/ui/hover-card";
import IntArrayBlock from "@/components/testcase_spec/blocks/int-array-block";
import TreeBlock from "@/components/testcase_spec/blocks/tree-block";
import {Popover, PopoverContent, PopoverTrigger} from "@/components/ui/popover";
import {Command, CommandEmpty, CommandGroup, CommandInput, CommandItem} from "@/components/ui/command";
import PresetButton from "@/components/preset/preset-button";

const Editor = () => {
  const context = useContext(TestcaseContext);
  if (!context) throw new Error("context 없음. 개판임");

  const { blocks, addBlock } = context;
  const child: Record<string, (blockIndex: number) => ReactNode> = {
    'Line': (blockIndex: number) => (<LineBlock blockIndex={blockIndex} key={blockIndex}/>),
    'Graph': (blockIndex: number) => (<GraphBlock blockIndex={blockIndex} key={blockIndex}/>),
    'Matrix': (blockIndex: number) => (<MatrixBlock blockIndex={blockIndex} key={blockIndex}/>),
    'String': (blockIndex: number) => (<StringBlock blockIndex={blockIndex} key={blockIndex}/>),
    'IntArray': (blockIndex: number) => (<IntArrayBlock blockIndex={blockIndex} key={blockIndex}/>),
    'Tree': (blockIndex: number) => (<TreeBlock blockIndex={blockIndex} key={blockIndex}/>),
  }

  const getBlockError: (blockIndex: number) => {color: string, content: string}[] = (blockIndex: number)=> {
      const currentBlock = blocks[blockIndex];
      const result: {color: string, content: string}[] = [];
      if (currentBlock.output.sequence.length === 0) {
          result.push({color: '#FACC15', content: "출력이 비어있습니다."})
      }
      return result;
  }

  const getBlockColor: (error: {color: string, content: string}[]) => string = (error: {color: string, content: string}[]) => {
      const keys = error.map(({color}) => color);
      if (keys.includes('#FACC15')) {
          return '#FACC15';
      }
      return '#000000';
  }

  return (
    <Card>
      <CardHeader className="relative">
        <CardTitle>테스트케이스 명세 설정</CardTitle>
        <CardDescription>테스트케이스가 어떻게 구성되어있는지 적는 공간입니다.</CardDescription>
        <div className="absolute top-4 right-4">
          <PresetButton />
        </div>
      </CardHeader>
      <CardContent>
        <div className="space-y-6 w-full max-w-4xl mx-auto px-4">
          <Accordion
            type="single"
            collapsible
            className="w-full"
          >
            {blocks.slice(1, blocks.length).map((block, i) => {
              const blockIndex = i+1; // 사전 설정 변수가 있으니까
              const error = getBlockError(blockIndex);
              return block.visibleType !== 'null' && (
                <div key={blockIndex}>
                  <AccordionItem value={`${blockIndex}`}>
                    <HoverCard>
                      <HoverCardTrigger asChild>
                        <AccordionTrigger className="hover:no-underline">
                          <b style={{ color: getBlockColor(error) }}>{blocks[blockIndex].visibleType}</b>
                        </AccordionTrigger>
                      </HoverCardTrigger>
                      <HoverCardContent side="top" align="end" sideOffset={8} className="bg-white shadow-xl border rounded-lg p-4">
                        <div>
                          <b>설정된 변수 및 범위</b>
                          {block.variable.slice(0, 3).map((variable, i) => (
                            <div key={i} className="flex items-center text-sm">
                              <span className="font-medium max-w-[5.5rem] truncate inline-block">
                                {variable.name ? variable.name : "설정 필요"}
                              </span>
                              <span className="mx-1">:</span>
                              <span className="font-semibold font-medium max-w-[5.5rem] truncate">
                                {variable.range.length
                                  ? `${variable.range[0].min} ~ ${variable.range[0].max}`
                                  : "설정 필요"}
                              </span>
                              {variable.range.length > 1 && <b>{" "}외 {variable.range.length-1}개</b>}
                            </div>
                          ))}
                          {block.variable.length > 3 && <div>{" "}외 {block.variable.length-3}개</div>}
                          {block.variable.length == 0 && <div>정의된 변수가 없습니다.</div>}
                        </div>

                        <div>
                          {error.length > 0 && <>
                            <b>에러</b>
                            {error.map(({color, content}, idx) => (
                                <div key={idx} style={{ color: color }}>{content}</div>
                            ))}
                          </>}
                        </div>
                      </HoverCardContent>
                    </HoverCard>
                    <AccordionContent>
                      {child[block.visibleType](blockIndex)}
                    </AccordionContent>
                  </AccordionItem>
                </div>
              )
            })}
          </Accordion>
          <Button className="mt-6 mx-auto block px-6 py-2 text-base" onClick={() => addBlock('Line')}>블럭 추가</Button>
        </div>
      </CardContent>
    </Card>
  );
};

export default Editor;
