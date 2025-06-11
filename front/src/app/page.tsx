"use client"

import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger
} from "@/components/ui/tabs";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle
} from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import CodeEditor from "@/components/code_editor/CodeEditor";
import React from "react";
import { TestcaseProvider } from "@/context/TestcaseContext";
import Editor from "@/components/testcase_spec/editor";

export default function Home() {
  const [code1, setCode1] = React.useState('');
  const [lang1, setLang1] = React.useState<'python'>('python');

  const [code2, setCode2] = React.useState('');
  const [lang2, setLang2] = React.useState<'python'>('python');

  return (
    <div className="max-w-4xl w-full mx-auto px-4 py-8">
      <TestcaseProvider>
        <Tabs defaultValue="일반 설정" className="space-y-6">
          <TabsList className="flex justify-center gap-4">
            <TabsTrigger value="일반 설정">일반 설정</TabsTrigger>
            <TabsTrigger value="테스트케이스 명세 설정">테스트케이스 명세 설정</TabsTrigger>
          </TabsList>

          <TabsContent value="일반 설정" className="mt-4">
            <Card>
              <CardHeader>
                <CardTitle>일반 설정</CardTitle>
                <CardDescription>코드 설정 및 반복 횟수를 설정하는 부분입니다.</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-1">
                  <Label>첫번째 코드</Label>
                  <CodeEditor code={code1} setCode={setCode1} language={lang1} setLang={setLang1} />
                </div>
                <div className="space-y-1">
                  <Label>두번째 코드</Label>
                  <CodeEditor code={code2} setCode={setCode2} language={lang2} setLang={setLang2} />
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="테스트케이스 명세 설정" className="mt-4">
            <Editor />
          </TabsContent>
        </Tabs>
      </TestcaseProvider>
    </div>
  );
}
