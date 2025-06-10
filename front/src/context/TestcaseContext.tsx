"use client";

import React, {createContext, ReactNode, useState} from "react";
import {VariableSpec} from "@/components/testcase_spec/variable";

interface BlockSpec {
  type: string;
  variables: VariableSpec[];
}

interface EditorContextType {
  variables: VariableSpec[][];
  setVariables: React.Dispatch<React.SetStateAction<VariableSpec[][]>>;
  blocks: BlockSpec[];
  setBlocks: React.Dispatch<React.SetStateAction<BlockSpec[]>>;
}

export const TestcaseContext = createContext<EditorContextType | null>(null);

export const TestcaseProvider = ({ children }: { children: ReactNode }) => {
  const [variables, setVariables] = useState<VariableSpec[][]>([[]]); // 사전설졍변수 있어서 이중으로 초기화
  const [blocks, setBlocks] = useState<BlockSpec[]>([]);
  // const [blocks, setBlocks] = useState([]);

  return (
    <TestcaseContext.Provider value={{ variables, setVariables, blocks, setBlocks }}>
      {children}
    </TestcaseContext.Provider>
  );
};
