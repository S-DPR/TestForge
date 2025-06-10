"use client";

import React, {createContext, ReactNode, useState} from "react";
import {VariableSpec} from "@/components/testcase_spec/variable";


interface EditorContextType {
  variables: VariableSpec[];
  setVariables: React.Dispatch<React.SetStateAction<VariableSpec[]>>;
  // blocks: any[];
  // setBlocks: React.Dispatch<React.SetStateAction<any[]>>;
}

const TestcaseContext = createContext<EditorContextType | null>(null);

export const TestcaseProvider = ({ children }: { children: ReactNode }) => {
  const [variables, setVariables] = useState<VariableSpec[]>([]);
  // const [blocks, setBlocks] = useState([]);

  return (
    <TestcaseContext.Provider value={{ variables, setVariables }}>
      {children}
    </TestcaseContext.Provider>
  );
};
