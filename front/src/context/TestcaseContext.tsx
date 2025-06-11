"use client";

import React, {createContext, ReactNode, useState} from "react";
import {VariableSpec} from "@/components/testcase_spec/variable";
import Output from "@/components/testcase_spec/output";
import {Range} from "@/components/testcase_spec/define-range";
import {LineConfig} from "@/components/testcase_spec/line-block";
import {GraphConfig} from "@/components/testcase_spec/graph-block";

export interface AbstractConfig {
  type: 'line' | 'graph';
}

type Config = LineConfig | GraphConfig;

interface BlockSpec {
  type: string;
  variables: VariableSpec[];
  output: Output;
  config: AbstractConfig;
}

interface EditorContextType {
  blocks: BlockSpec[];
  setBlocks: React.Dispatch<React.SetStateAction<BlockSpec[]>>;

  addVariable: (blockIndex: number, variable: VariableSpec) => void;
  updateVariable: (blockIndex: number, variableIndex: number, variable: VariableSpec) => void;
  removeVariable: (blockIndex: number, variableIndex: number) => void;

  addVariableRange: (blockIndex: number, variableIndex: number, range: Range) => void;
  updateVariableRange: (blockIndex: number, variableIndex: number, rangeIndex: number, range: Range) => void;

  addBlock: (type: string) => void;
  addOutputSequence: (blockIndex: number) => void;
  updateOutputSequence: (blockIndex: number, sequenceIndex: number, value: string) => void;
  updateBlockType: (blockIndex: number, type: string) => void;
}

export const TestcaseContext = createContext<EditorContextType | null>(null);

export const TestcaseProvider = ({ children }: { children: ReactNode }) => {
  const [blocks, setBlocks] = useState<BlockSpec[]>([{ type: 'null', variables: [], output: { sequence: [], separator: '' }, config: {} as LineConfig }]);

  const addVariable = (blockIndex: number, variable: VariableSpec) => {
    console.log("hihi")
    setBlocks((prev) => {
      const newBlocks = structuredClone(prev);
      newBlocks[blockIndex].variables.push(variable);
      console.log(newBlocks)
      return newBlocks;
    })
  }

  const updateVariable = (blockIndex: number, variableIndex: number, variable: VariableSpec) => {
    setBlocks((prev) => {
      const newBlocks = structuredClone(prev);
      newBlocks[blockIndex].variables[variableIndex] = variable;
      return newBlocks;
    })
  }

  const removeVariable = (blockIndex: number, variableIndex: number) => {
    setBlocks((prev) => {
      const newBlocks = structuredClone(prev);
      newBlocks[blockIndex].variables = newBlocks[blockIndex].variables.filter((_, idx) => idx !== variableIndex);
      return newBlocks;
    })
  }

  const addVariableRange = (blockIndex: number, variableIndex: number, range: Range) => {
    setBlocks((prev) => {
      const newBlocks = structuredClone(prev);
      newBlocks[blockIndex].variables[variableIndex].ranges.push(range);
      return newBlocks;
    })
  }

  const updateVariableRange = (blockIndex: number, variableIndex: number, rangeIndex: number, range: Range) => {
    setBlocks((prev) => {
      const newBlocks = structuredClone(prev);
      newBlocks[blockIndex].variables[variableIndex].ranges[rangeIndex] = range;
      return newBlocks;
    })
  }

  // const addVariable = (blockIndex: number, variable: VariableSpec) => {
  //   setVariables((prev) => {
  //     const newVariable = structuredClone(prev);
  //     newVariable[blockIndex].push(variable);
  //     return newVariable;
  //   });
  // };
  //
  // const initVariables = (blockIndex: number) => {
  //   setVariables((prev) => {
  //     const newVariable = structuredClone(prev);
  //     newVariable[blockIndex] = []
  //     return newVariable;
  //   })
  // }

  // const updateVariables = (blockIndex: number, variableIndex: number, field: string, value: string)=> {
  //   const updateMap: Record<string, (data: VariableSpec[][]) => void> = {
  //     'type': (newVariable: VariableSpec[][]) => newVariable[blockIndex][variableIndex].type = value,
  //     'name': (newVariable: VariableSpec[][]) => newVariable[blockIndex][variableIndex].name = value,
  //   }

  //   setVariables((prev) => {
  //     const newVariable = structuredClone(prev);
  //     updateMap[field](newVariable);
  //     return newVariable;
  //   })
  // }
  //
  // const addVariableRange = (blockIndex: number, variableIndex: number) => {
  //   setVariables((prev) => {
  //     const newVariable = structuredClone(prev);
  //     newVariable[blockIndex][variableIndex].ranges.push({ min: '0', max: '0' })
  //     return newVariable;
  //   });
  // };

  // const updateVariablesRange = (blockIndex: number, variableIndex: number, rangeIndex: number, field: string, value: string)=> {
  //   const updateMap: Record<string, (data: VariableSpec[][]) => void> = {
  //     'min': (newVariable: VariableSpec[][]) => newVariable[blockIndex][variableIndex].ranges[rangeIndex].min = value,
  //     'max': (newVariable: VariableSpec[][]) => newVariable[blockIndex][variableIndex].ranges[rangeIndex].max = value,
  //   }
  //
  //   setVariables((prev) => {
  //     const newVariable = structuredClone(prev);
  //     updateMap[field](newVariable);
  //     return newVariable;
  //   })
  // }

  const addOutputSequence = (blockIndex: number) => {
    setBlocks((prev) => {
      const newBlocks = structuredClone(prev);
      newBlocks[blockIndex].output.sequence.push('')
      return newBlocks;
    })
  }

  const updateOutputSequence = (blockIndex: number, sequenceIndex: number, value: string) => {
    setBlocks((prev) => {
      const newBlocks = structuredClone(prev);
      newBlocks[blockIndex].output.sequence[sequenceIndex] = value;
      return newBlocks;
    })
  }

  const configs: Record<string, Config> = {
    'line': {} as LineConfig,
    'graph': {
      nodeCount: "",
      edgeCount: "",
      weightRange: {min: '0', max: '10'},
      isPerfect: false,
      isConnect: false,
      isCycle: false
    } as GraphConfig
  }

  const addBlock = (type: string) => {
    setBlocks((prev) => [
      ...prev,
      { type: type, variables: [], output: {sequence: [], separator: ' '}, config: configs[type] }
    ])
  }

  const updateBlockType = (blockIndex: number, type: string) => {
    setBlocks((prev) => {
      const newBlocks = structuredClone(prev);
      newBlocks[blockIndex].type = type;
      newBlocks[blockIndex].config = configs[type];
      return newBlocks;
    })
  }

  // const removeVariable = (blockIndex: number, variableIndex: number) => {
  //   setVariables((prev) => {
  //     const newVariable = structuredClone(prev);
  //     newVariable[blockIndex] = newVariable[blockIndex].filter((_, idx) => idx !== variableIndex);
  //     return newVariable;
  //   });
  // };

  return (
    <TestcaseContext.Provider value={{
      blocks, setBlocks, addVariable, updateVariable, removeVariable, addVariableRange, updateVariableRange, addBlock, addOutputSequence, updateOutputSequence, updateBlockType
    }}>
      {children}
    </TestcaseContext.Provider>
  );
};
