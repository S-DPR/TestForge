import {Card, CardContent, CardDescription, CardHeader, CardTitle} from "@/components/ui/card";
import {Label} from "@/components/ui/label";
import CodeEditor from "@/components/code_editor/CodeEditor";
import React, {useContext} from "react";
import {CodeContext} from "@/context/CodeContext";

const GeneralSetting = () => {
    const ctx = useContext(CodeContext);
    if (!ctx) throw new Error("No code context.");

    const { code1, setCode1, lang1, setLang1 } = ctx;
    const { code2, setCode2, lang2, setLang2 } = ctx;

    return (
        <Card>
            <CardHeader>
                <CardTitle>일반 설정</CardTitle>
                <CardDescription>비교할 두 코드 및 반복 횟수를 설정하는 부분입니다.</CardDescription>
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
    );
}

export default GeneralSetting;
