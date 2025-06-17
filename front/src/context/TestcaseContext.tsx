"use client";

import React, {createContext, ReactNode, useState} from "react";
import {VariableSpec} from "@/components/testcase_spec/variable";
import {OutputType} from "@/components/testcase_spec/output";
import {Range} from "@/components/testcase_spec/define-range";
import {LineConfig} from "@/components/testcase_spec/blocks/line-block";
import {GraphConfig} from "@/components/testcase_spec/blocks/graph-block";
import {MatrixConfig} from "@/components/testcase_spec/blocks/matrix-block";

export interface AbstractConfig {
  type: 'line' | 'graph' | 'matrix';
}

type Config = LineConfig | GraphConfig | MatrixConfig;

export interface BlockSpec {
  type: string; // 실제 타입
  visibleType: string; // ui상 보이는 타입
  variables: VariableSpec[];
  output: OutputType;
  config: AbstractConfig;
  repeat: string;
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
  updateOutputSequence: (blockIndex: number, sequenceIndex: number, sequence: string[]) => void;
  removeOutputSequence: (blockIndex: number, sequenceIndex: number) => void;

  updateBlockType: (blockIndex: number, type: string) => void;
  deleteBlockType: (blockIndex: number) => void;
  updateBlockRepeat: (blockIndex: number, value: string) => void;
  updateSeparator: (blockIndex: number, value: string) => void;
}

export const TestcaseContext = createContext<EditorContextType | null>(null);

export const TestcaseProvider = ({ children }: { children: ReactNode }) => {
  const [blocks, setBlocks] = useState<BlockSpec[]>([{ type: 'null', visibleType: 'null', variables: [], output: { sequence: [], separator: '' }, config: {} as LineConfig, repeat: '' }]);

  const addVariable = (blockIndex: number, variable: VariableSpec) => {
    setBlocks((prev) => {
      const newBlocks = structuredClone(prev);
      newBlocks[blockIndex].variables.push(variable);
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

  const addOutputSequence = (blockIndex: number) => {
    setBlocks((prev) => {
      const newBlocks = structuredClone(prev);
      newBlocks[blockIndex].output.sequence.push('')
      return newBlocks;
    })
  }

  const updateOutputSequence = (blockIndex: number, sequenceIndex: number, sequence: string[]) => {
    setBlocks((prev) => {
      const newBlocks = structuredClone(prev);
      newBlocks[blockIndex].output.sequence = sequence;
      return newBlocks;
    })
  }

  const removeOutputSequence = (blockIndex: number, sequenceIndex: number) => {
    setBlocks((prev) => {
      const newBlocks = structuredClone(prev);
      newBlocks[blockIndex].output.sequence = newBlocks[blockIndex].output.sequence.filter((_, idx) => idx !== sequenceIndex);
      return newBlocks;
    })
  }

  const updateSeparator = (blockIndex: number, value: string) => {
    setBlocks((prev) => {
      const newBlocks = structuredClone(prev);
      newBlocks[blockIndex].output.separator = value;
      return newBlocks;
    })
  }

  const configs: (type: string) => Config = (type: string) => {
    switch (type) {
      case 'graph':
        return {
          type: 'graph',
          nodeCount: "",
          edgeCount: "",
          weightRange: [],
          isPerfect: false,
          isConnect: false,
          isCycle: false
        } as GraphConfig
      case 'matrix':
        return {
          type: 'matrix',
          colSize: "",
          rowSize: "1",
          numType: "int",
          numRange: [],
          isDistinct: false,
          valueLimit: {},
          emptyValue: null,
          randomEmpty: false,
          isGraph: false,
          isSymmetric: false
        } as MatrixConfig
      case 'line':
      default:
        return {} as LineConfig;
    }
  }

  const typeMapping: Record<string, string> = {
    // base
    Line: 'line',
    Graph: 'graph',
    Matrix: 'matrix',
    // using
    String: 'matrix',
    IntArray: 'matrix',
  }

  const addBlock = (type: string) => {
    setBlocks((prev) => [
      ...prev,
      { type: typeMapping[type], visibleType: type, variables: [], output: {sequence: [], separator: ' '}, config: configs(typeMapping[type]), repeat: '1' }
    ])
  }

  const updateBlockType = (blockIndex: number, type: string) => {
    setBlocks((prev) => {
      const newBlocks = structuredClone(prev);
      newBlocks[blockIndex].type = typeMapping[type];
      newBlocks[blockIndex].visibleType = type;
      newBlocks[blockIndex].config = configs(typeMapping[type]);
      return newBlocks;
    })
  }

  const updateBlockRepeat = (blockIndex: number, value: string) => {
    setBlocks((prev) => {
      const newBlocks = structuredClone(prev);
      newBlocks[blockIndex].repeat = value;
      return newBlocks;
    })
  }

  const deleteBlockType = (blockIndex: number) => {
    setBlocks((prev) => {
      let newBlocks = structuredClone(prev);
      newBlocks = newBlocks.filter((_, idx) => idx !== blockIndex);
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
      blocks, setBlocks, addVariable, updateVariable, removeVariable, addVariableRange, updateVariableRange, addBlock, addOutputSequence, updateOutputSequence, updateBlockType, updateBlockRepeat, updateSeparator, removeOutputSequence, deleteBlockType
    }}>
      {children}
    </TestcaseContext.Provider>
  );
};
