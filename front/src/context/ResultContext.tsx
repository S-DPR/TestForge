import React, {createContext, ReactNode, useState} from "react";

export interface Result {
  filename: string;
  diffStatus: string;
}

interface ResultContextType {
  results: Result[];
  setResults: (results: Result[]) => void;
  addResult: (result: Result) => void;
  initResult: () => void;

  inputDialogOpen: boolean;
  setInputDialogOpen: (open: boolean) => void;

  inputSelected: string | null;
  setInputSelected: (selected: string) => void;
}

export const ResultContext = createContext<ResultContextType | null>(null);

const ResultProvider = ({ children }: { children: ReactNode }) => {
  const [ results, setResults ] = React.useState<Result[]>([]);
  const [inputDialogOpen, setInputDialogOpen] = useState(false);
  const [inputSelected, setInputSelected] = useState<string | null>(null);

  const addResult = (result: Result) => {
    setResults((prev) => {
      const newResults = structuredClone(prev);
      newResults.push(result);
      return newResults;
    })
  }
  const initResult = () => {
    setResults([])
  }

  return (<ResultContext.Provider value={{ results, addResult, setResults, initResult, inputDialogOpen, setInputDialogOpen, inputSelected, setInputSelected }}>
      {children}
    </ResultContext.Provider>
  );
}

export default ResultProvider;
