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

interface BlockWrapperProps {
  blockIndex: number;
  children: ReactNode;
}

const BlockWrapper = ({ blockIndex, children }: BlockWrapperProps) => {
  const ctx = useContext(TestcaseContext);
  if (!ctx) throw new Error('콘텍스트없서요');

  const { blocks, updateBlockType, deleteBlockType } = ctx;

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
              <SelectItem value="line">Line</SelectItem>
              <SelectItem value="graph">Graph</SelectItem>
              <SelectItem value="matrix">Matrix</SelectItem>
              <SelectItem value="string">String</SelectItem>
            </SelectGroup>
          </SelectContent>
        </Select>
      </CardHeader>
      <CardContent className="pt-4">
        {children}
      </CardContent>
      <Button className="bg-red-600 hover:bg-red-700 text-white" onClick={() => {deleteBlockType(blockIndex)}}>블럭 삭제</Button>
    </Card>
  )
}

export default BlockWrapper;
