import {Card, CardContent, CardDescription, CardHeader, CardTitle} from "@/components/ui/card";
import {Label} from "@/components/ui/label";
import CodeEditor from "@/components/code_editor/CodeEditor";
import React, {useContext} from "react";
import {CodeContext} from "@/context/CodeContext";
import {Input} from "@/components/ui/input";

const GeneralSetting = () => {
    const ctx = useContext(CodeContext);
    if (!ctx) throw new Error("No code context.");

    const { code1, setCode1, lang1, setLang1 } = ctx;
    const { code2, setCode2, lang2, setLang2 } = ctx;
    const { repeatCount, setRepeatCount } = ctx;

    return (
        <Card>
            <CardHeader>
                <CardTitle>일반 설정</CardTitle>
                <CardDescription>비교할 두 코드 및 반복 횟수를 설정하는 공간입니다.</CardDescription>
            </CardHeader>
          <CardContent>
            <div className="space-y-6">
              <Card className="p-4">
                <CardHeader className="p-0 pb-2">
                  <CardTitle>반복 횟수 설정</CardTitle>
                  <CardDescription>무작위 테스트를 몇 번 할지 설정합니다. 한 번에 최대 50회까지 반복할 수 있습니다.</CardDescription>
                </CardHeader>
                <Input
                  type="number"
                  value={repeatCount}
                  min={1}
                  max={50}
                  onChange={(e) => setRepeatCount(e.target.valueAsNumber)}
                />
              </Card>

              <Card className="p-4">
                <CardHeader className="p-0 pb-2">
                  <CardTitle>첫번째 코드</CardTitle>
                </CardHeader>
                <CodeEditor code={code1} setCode={setCode1} language={lang1} setLang={setLang1} />
              </Card>

              <Card className="p-4">
                <CardHeader className="p-0 pb-2">
                  <CardTitle>두번째 코드</CardTitle>
                </CardHeader>
                <CodeEditor code={code2} setCode={setCode2} language={lang2} setLang={setLang2} />
              </Card>
            </div>
          </CardContent>
        </Card>
    );
}

export default GeneralSetting;
