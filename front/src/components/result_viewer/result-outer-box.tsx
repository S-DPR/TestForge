import React, {ReactNode, useContext} from "react";
import {TestcaseContext} from "@/context/TestcaseContext";
import LineBlock from "@/components/testcase_spec/blocks/line-block";
import GraphBlock from "@/components/testcase_spec/blocks/graph-block";
import MatrixBlock from "@/components/testcase_spec/blocks/matrix-block";
import BlockWrapper from "@/components/testcase_spec/block-wrapper";
import {Button} from "@/components/ui/button";
import ResultBox from "@/components/result_viewer/result-box";
import {Card, CardContent, CardDescription, CardHeader, CardTitle} from "@/components/ui/card";

const Editor = () => {
  return (
    <Card>
      <CardHeader>
        <CardTitle>결과 확인</CardTitle>
        <CardDescription>비교 결과를 확인하는 공간입니다. 클릭하면 어떤 데이터가 사용되었는지 확인이 가능합니다.</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-6 w-full max-w-4xl mx-auto px-4">
          <ResultBox></ResultBox>
        </div>
      </CardContent>
    </Card>
  );
};

export default Editor;
