import {useContext} from "react";
import {AbstractConfig, TestcaseContext} from "@/context/TestcaseContext";
import BlockWrapper from "@/components/testcase_spec/block-wrapper";

export interface LineConfig extends AbstractConfig {
  _: null;
}

interface LineBlockProps {
  blockIndex: number;
}

const LineBlock = ({ blockIndex }: LineBlockProps) => {
  const ctx = useContext(TestcaseContext);
  if (!ctx) throw new Error('근데 이거 계속 반복되네');

  return (
    <BlockWrapper blockIndex={blockIndex} isRenderOutput={true} />
  )
}

export default LineBlock;
