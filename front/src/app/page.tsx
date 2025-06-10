"use client"

import {Tabs, TabsContent, TabsList, TabsTrigger} from "@/components/ui/tabs";
import {Card, CardContent, CardDescription, CardHeader, CardTitle} from "@/components/ui/card";
import {Label} from "@/components/ui/label";
import CodeEditor from "@/components/code_editor/CodeEditor";
import React, {useContext} from "react";
import {TestcaseContext, TestcaseProvider} from "@/context/TestcaseContext";
import {Button} from "@/components/ui/button";
import LineBlock from "@/components/testcase_spec/line-block";

export default function Home() {
  const [code1, setCode1] = React.useState('')
  const [lang1, setLang1] = React.useState<'python'>('python')

  const [code2, setCode2] = React.useState('')
  const [lang2, setLang2] = React.useState<'python'>('python')

  return (
    <>
      <div className="flex w-full max-w-sm flex-col gap-6">
        <Tabs defaultValue="일반 설정">
          <TabsList>
            <TabsTrigger value={"일반 설정"}>일반 설정</TabsTrigger>
            <TabsTrigger value={"테스트케이스 명세 설정"}>테스트케이스 명세 설정</TabsTrigger>
          </TabsList>
          <TabsContent value={"일반 설정"}>
            <Card>
              <CardHeader>
                <CardTitle>일반 설정</CardTitle>
                <CardDescription>코드 설정 및 반복 횟수를 설정하는 부분입니다.</CardDescription>
              </CardHeader>
              <CardContent>
                <Label>첫번째 코드</Label>
                <CodeEditor code={code1} setCode={setCode1} language={lang1} setLang={setLang1}></CodeEditor>
              </CardContent>
              <CardContent>
                <Label>두번째 코드</Label>
                <CodeEditor code={code2} setCode={setCode2} language={lang2} setLang={setLang2}></CodeEditor>
              </CardContent>
            </Card>
          </TabsContent>
          <TabsContent value={"테스트케이스 명세 설정"}>
            <TestcaseProvider>
              <Editor />
            </TestcaseProvider>
          </TabsContent>
        </Tabs>
      </div>
    </>
  );
}

const Editor = () => {
  const context = useContext(TestcaseContext);
  if (!context) throw new Error("context 없음. 개판임");

  const { variables, setVariables, blocks, setBlocks } = context;

  const addVariable = (blockIndex: number) => {
    setVariables((prev) => {
      const newVariable = prev.map(i => i.map(j => ({ ...j })));
      newVariable[blockIndex].push({ name: "", type: "", ranges: [[]] })
      return newVariable;
    });
  };

  const addBlock = (type: string) => {
    setBlocks((prev) => [
        ...prev,
      { type: type, variables: [] }
    ])
  }

  const removeVariable = (blockIndex: number, variableIndex: number) => {
    setVariables((prev) => {
      const newVariable = prev.map(i => i.map(j => ({...j})));
      newVariable[blockIndex] = newVariable[blockIndex].filter((_, idx) => idx !== variableIndex);
      return newVariable;
    });
  };

  return (
      <>
        {blocks.map((block, i) => {
          if (!variables[i]) variables[i] = [];
          return (
              <LineBlock key={i} blockIndex={i} variables={variables[i]} onVariableAddClick={addVariable} onRemoveVariable={removeVariable}></LineBlock>
          )
        })}
        <Button onClick={() => addBlock('type')}>블럭 추가</Button>
      </>
  );
};
