import React, {ReactNode, useContext} from "react";
import {TestcaseContext} from "@/context/TestcaseContext";
import LineBlock from "@/components/testcase_spec/line-block";
import GraphBlock from "@/components/testcase_spec/graph-block";
import MatrixBlock from "@/components/testcase_spec/matrix-block";
import BlockWrapper from "@/components/testcase_spec/block-wrapper";
import {Button} from "@/components/ui/button";

const Editor = () => {
  const context = useContext(TestcaseContext);
  if (!context) throw new Error("context 없음. 개판임");

  const { blocks, addBlock } = context;
  const child: Record<string, (blockIndex: number) => ReactNode> = {
    'line': (blockIndex: number) => (<LineBlock blockIndex={blockIndex} key={blockIndex}/>),
    'graph': (blockIndex: number) => (<GraphBlock blockIndex={blockIndex} key={blockIndex}/>),
    'matrix': (blockIndex: number) => (<MatrixBlock blockIndex={blockIndex} key={blockIndex}/>),
  }

  return (
    <>
      {blocks.slice(1, blocks.length).map((block, i) => {
        const blockIndex = i+1; // 사전 설정 변수가 있으니까
        return block.type !== 'null' && (
          <BlockWrapper key={`block-${blockIndex}`} blockIndex={blockIndex}>
            {child[block.type](blockIndex)}
          </BlockWrapper>
        )
      })}
      <Button onClick={() => addBlock('line')}>블럭 추가</Button>
    </>
  );
};

export default Editor;
