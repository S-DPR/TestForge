import React, {ReactNode, useContext} from "react";
import {TestcaseContext} from "@/context/TestcaseContext";
import LineBlock from "@/components/testcase_spec/blocks/line-block";
import GraphBlock from "@/components/testcase_spec/blocks/graph-block";
import MatrixBlock from "@/components/testcase_spec/blocks/matrix-block";
import BlockWrapper from "@/components/testcase_spec/block-wrapper";
import {Button} from "@/components/ui/button";
import {Card, CardContent, CardDescription, CardHeader, CardTitle} from "@/components/ui/card";
import StringBlock from "@/components/testcase_spec/blocks/string-block";

const Editor = () => {
  const context = useContext(TestcaseContext);
  if (!context) throw new Error("context 없음. 개판임");

  const { blocks, addBlock } = context;
  const child: Record<string, (blockIndex: number) => ReactNode> = {
    'line': (blockIndex: number) => (<LineBlock blockIndex={blockIndex} key={blockIndex}/>),
    'graph': (blockIndex: number) => (<GraphBlock blockIndex={blockIndex} key={blockIndex}/>),
    'matrix': (blockIndex: number) => (<MatrixBlock blockIndex={blockIndex} key={blockIndex}/>),
    'string': (blockIndex: number) => (<StringBlock blockIndex={blockIndex} key={blockIndex}/>),
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>테스트케이스 명세 설정</CardTitle>
        <CardDescription>테스트케이스가 어떻게 구성되어있는지 적는 공간입니다.</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-6 w-full max-w-4xl mx-auto px-4">
          {blocks.slice(1, blocks.length).map((block, i) => {
            const blockIndex = i+1; // 사전 설정 변수가 있으니까
            return block.visibleType !== 'null' && (
              <BlockWrapper key={`block-${blockIndex}`} blockIndex={blockIndex}>
                {child[block.visibleType](blockIndex)}
              </BlockWrapper>
            )
          })}
          <Button className="mt-6 mx-auto block px-6 py-2 text-base" onClick={() => addBlock('line')}>블럭 추가</Button>
        </div>
      </CardContent>
    </Card>
  );
};

export default Editor;
