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

  addVariable: (blockIndex: number) => void;
  updateVariables: (blockIndex: number, variableIndex: number, field: string, value: string) => void;
  addVariableRange: (blockIndex: number, variableIndex: number) => void;
  updateVariablesRange: (blockIndex: number, variableIndex: number, rangeIndex: number, field: string, value: string) => void;
  removeVariable: (blockIndex: number, variableIndex: number) => void;
  addBlock: (type: string) => void;
}

export const TestcaseContext = createContext<EditorContextType | null>(null);

export const TestcaseProvider = ({ children }: { children: ReactNode }) => {
  const [variables, setVariables] = useState<VariableSpec[][]>([[]]); // 사전설졍변수 있어서 이중으로 초기화
  const [blocks, setBlocks] = useState<BlockSpec[]>([]);

  const addVariable = (blockIndex: number) => {
    setVariables((prev) => {
      const newVariable = prev.map(i => i.map(j => ({ ...j, ranges: [...j.ranges] })));
      newVariable[blockIndex].push({ name: "", type: "", ranges: [] })
      return newVariable;
    });
  };

  const updateVariables = (blockIndex: number, variableIndex: number, field: string, value: string)=> {
    const updateMap: Record<string, (data: VariableSpec[][]) => void> = {
      'type': (newVariable: VariableSpec[][]) => newVariable[blockIndex][variableIndex].type = value,
      'name': (newVariable: VariableSpec[][]) => newVariable[blockIndex][variableIndex].name = value,
    }

    setVariables((prev) => {
      const newVariable = prev.map(i => i.map(j => ({ ...j, ranges: [...j.ranges] })));
      updateMap[field](newVariable);
      return newVariable;
    })
  }

  const addVariableRange = (blockIndex: number, variableIndex: number) => {
    setVariables((prev) => {
      const newVariable = prev.map(i => i.map(j => ({ ...j, ranges: [...j.ranges] })));
      newVariable[blockIndex][variableIndex].ranges.push({ min: '0', max: '0' })
      return newVariable;
    });
  };

  const updateVariablesRange = (blockIndex: number, variableIndex: number, rangeIndex: number, field: string, value: string)=> {
    const updateMap: Record<string, (data: VariableSpec[][]) => void> = {
      'min': (newVariable: VariableSpec[][]) => newVariable[blockIndex][variableIndex].ranges[rangeIndex].min = value,
      'max': (newVariable: VariableSpec[][]) => newVariable[blockIndex][variableIndex].ranges[rangeIndex].max = value,
    }

    setVariables((prev) => {
      const newVariable = prev.map(i => i.map(j => ({ ...j, ranges: [...j.ranges] })));
      updateMap[field](newVariable);
      return newVariable;
    })
  }

  const addBlock = (type: string) => {
    setBlocks((prev) => [
      ...prev,
      { type: type, variables: [] }
    ])
  }

  const removeVariable = (blockIndex: number, variableIndex: number) => {
    setVariables((prev) => {
      const newVariable = prev.map(i => i.map(j => ({ ...j, ranges: [...j.ranges] })));
      newVariable[blockIndex] = newVariable[blockIndex].filter((_, idx) => idx !== variableIndex);
      return newVariable;
    });
  };

  return (
    <TestcaseContext.Provider value={{
      variables, setVariables, blocks, setBlocks, addVariable, updateVariables, addVariableRange, updateVariablesRange, addBlock, removeVariable
    }}>
      {children}
    </TestcaseContext.Provider>
  );
};
