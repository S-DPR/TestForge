import {Button} from "@/components/ui/button";
import {BlockSpec, TestcaseContext} from "@/context/TestcaseContext";
import {useContext} from "react";
import {CodeContext} from "@/context/CodeContext";

const SubmitTestcaseRequestButton = () => {
    const tcCtx = useContext(TestcaseContext);
    const codeCtx = useContext(CodeContext);
    if (!tcCtx) throw new Error("또 tc ctx에러야");
    if (!codeCtx) throw new Error("또 code ctx 에러야");

    const { blocks } = tcCtx;
    const { code1, lang1, code2, lang2 } = codeCtx;

    return <Button onClick={() => {
        console.log('c1', code1);
        console.log('c2', code2);
        sendRequest(buildPayload(code1, lang1, code2, lang2, blocks), 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ5NzQxOTQ3LCJpYXQiOjE3NDk3NDE2NDcsImp0aSI6IjAzNTE4NDlkZjA3YTRhMTZhMTIzMWYzYThkMTM2MDc0IiwidXNlcl9pZCI6IjYyZGUwZjVlLTM2MzQtNGQ0Mi1iMWRlLThkYTdiMzExYzA4MyJ9.dFuV1ng4WzwTx2_3k0VkAE6nChfDf6MlVkFfiaej7A4')
    }}>제출</Button>
}

const sendRequest = async (payload: object, token: string) => {
    try {
        const res = await fetch('http://localhost:9001/test-execute', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'text/event-stream',
                "Authorization": token
            },
            body: JSON.stringify(payload)
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
                if (eventStr) console.log(eventStr);
            }
        }
    } catch (err) {
        console.error(err);
    }
}

const buildPayload = (code1: string, lang1: string, code2: string, lang2: string, blocks: BlockSpec[]) => {
    return {
        TestcaseFormat: {
            variable_format: [],
            lines: blocks.slice(1, blocks.length)
        },
        Code1: code1,
        Code2: code2,
        TimeLimit: 1,
        RepeatCount: 50,
    }
}

export default SubmitTestcaseRequestButton;