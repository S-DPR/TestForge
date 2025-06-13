"use client"

import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger
} from "@/components/ui/tabs";
import React from "react";
import { TestcaseProvider } from "@/context/TestcaseContext";
import Editor from "@/components/testcase_spec/editor";
import SubmitTestcaseRequestButton from "@/components/testcase_spec/submit-testcase-request-button";
import CodeProvider from "@/context/CodeContext";
import GeneralSetting from "@/components/code_editor/general-setting";
import ResultProvider from "@/context/ResultContext";
import ResultOuterBox from "@/components/result_viewer/result-outer-box";
import ResultInputDialog from "@/components/result_viewer/result-input-dialog";

export default function Home() {
  return (
    <div className="max-w-4xl w-full mx-auto px-4 py-8">
      <CodeProvider>
        <TestcaseProvider>
          <ResultProvider>
            <Tabs defaultValue="일반 설정" className="space-y-6">
              <TabsList className="flex justify-center gap-4">
                <TabsTrigger value="일반 설정">일반 설정</TabsTrigger>
                <TabsTrigger value="테스트케이스 명세 설정">테스트케이스 명세 설정</TabsTrigger>
                <TabsTrigger value="결과 확인">결과 확인</TabsTrigger>
              </TabsList>

                <TabsContent value="일반 설정" className="mt-4">
                  <GeneralSetting />
                </TabsContent>

                <TabsContent value="테스트케이스 명세 설정" className="mt-4">
                  <Editor />
                </TabsContent>

                <TabsContent value="결과 확인" className="mt-4">
                  <ResultInputDialog/>
                  <ResultOuterBox/>
                </TabsContent>
            </Tabs>
            <SubmitTestcaseRequestButton />
          </ResultProvider>
        </TestcaseProvider>
      </CodeProvider>
    </div>
  );
}
