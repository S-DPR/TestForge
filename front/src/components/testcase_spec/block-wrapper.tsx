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
import React, {ReactNode, useContext, useEffect} from "react";
import {TestcaseContext} from "@/context/TestcaseContext";

interface BlockWrapperProps {
  blockIndex: number;
  children: ReactNode;
}

const BlockWrapper = ({ blockIndex, children }: BlockWrapperProps) => {
  const ctx = useContext(TestcaseContext);
  if (!ctx) throw new Error('콘텍스트없서요');

  const { blocks, updateBlockType } = ctx;

  return (
    <Card>
      <CardHeader>
        <Select value={blocks[blockIndex]?.type ?? 'line'} onValueChange={(type: 'line' | 'graph') => updateBlockType(blockIndex, type)}>
          <SelectTrigger className="w-[180px] border-gray-600 rounded-md px-3 py-2">
            <SelectValue placeholder="블럭 타입 선택" />
          </SelectTrigger>
          <SelectContent className="bg-white border border-gray-700">
            <SelectGroup>
              <SelectLabel>타입</SelectLabel>
              <SelectItem value="line">Line</SelectItem>
              <SelectItem value="graph">Graph</SelectItem>
            </SelectGroup>
          </SelectContent>
        </Select>
      </CardHeader>
      <CardContent>
        {children}
      </CardContent>
    </Card>
  )
}

export default BlockWrapper;
