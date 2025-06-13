import {Button} from "@/components/ui/button";
import {BlockSpec, TestcaseContext} from "@/context/TestcaseContext";
import {useContext} from "react";
import {CodeContext} from "@/context/CodeContext";
import {Result, ResultContext} from "@/context/ResultContext";

const SubmitTestcaseRequestButton = () => {
    const tcCtx = useContext(TestcaseContext);
    const codeCtx = useContext(CodeContext);
    const resultCtx = useContext(ResultContext);
    if (!tcCtx) throw new Error("또 tc ctx 에러야");
    if (!codeCtx) throw new Error("또 code ctx 에러야");
    if (!resultCtx) throw new Error("또 result ctx 에러야");

    const { blocks } = tcCtx;
    const { code1, lang1, code2, lang2, repeatCount } = codeCtx;
    const { addResult, initResult } = resultCtx;

    return <Button onClick={() => {
        initResult()
        sendRequest(buildPayload(code1, lang1, code2, lang2, repeatCount, blocks), addResult)
    }}>제출</Button>
}

const sendRequest = async (payload: object, addResult: (result: Result) => void) => {
    try {
        const res = await fetch('http://localhost:9001/test-execute', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'text/event-stream',
            },
            body: JSON.stringify(payload),
            credentials: "include"
        });
        if (res.body == null) {
            console.log('nooo');
            return;
        }

        const reader = res.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            buffer += decoder.decode(value, { stream: true });
            let idx;
            while ((idx = buffer.indexOf('\n\n')) >= 0) {
                const eventStr = buffer.slice(0, idx).trim();
                buffer = buffer.slice(idx + 2);
                if (eventStr) addResult(handleEvent(eventStr));
            }
        }
    } catch (err) {
        console.error(err);
    }
}

const buildPayload = (code1: string, lang1: string, code2: string, lang2: string, repeatCount: number, blocks: BlockSpec[]) => {
    return {
        TestcaseFormat: {
            variable_format: [],
            lines: blocks.slice(1, blocks.length)
        },
        Code1: code1,
        Code2: code2,
        TimeLimit: 1,
        RepeatCount: repeatCount,
    }
}

const handleEvent = (eventStr: string): Result => {
    const lines = eventStr.split(/\r?\n/);
    // let type = '';
    let data = '';
    for (const line of lines) {
        if (line.startsWith('event:')) {
            // type = line.slice(6).trim();
        } else if (line.startsWith('data:')) {
            data += line.slice(5).trim();
        }
    }
    const obj = JSON.parse(data);
    return { filename: obj.filename, diffStatus: obj.diffStatus };
}

export default SubmitTestcaseRequestButton;