import {Button} from "@/components/ui/button";
import {BlockSpec, TestcaseContext} from "@/context/TestcaseContext";
import {useContext} from "react";
import {CodeContext} from "@/context/CodeContext";
import {Result, ResultContext} from "@/context/ResultContext";
import {toast} from "sonner";
import {HTTP_METHOD, LoginContext} from "@/context/LoginContext";

const SubmitTestcaseRequestButton = () => {
    const tcCtx = useContext(TestcaseContext);
    const codeCtx = useContext(CodeContext);
    const resultCtx = useContext(ResultContext);
    const loginCtx = useContext(LoginContext);

    if (!tcCtx) throw new Error("또 tc ctx 에러야");
    if (!codeCtx) throw new Error("또 code ctx 에러야");
    if (!resultCtx) throw new Error("또 result ctx 에러야");
    if (!loginCtx) throw new Error("또또또 login 콘텍스트 에러야");

    const { blocks } = tcCtx;
    const { code1, lang1, code2, lang2, repeatCount } = codeCtx;
    const { addResult, initResult } = resultCtx;
    const { request } = loginCtx;


    const sendRequest = async (payload: object) => {
        try {
            const res = await request({
                url: 'http://localhost:9001/test-execute',
                method: HTTP_METHOD.POST,
                body: payload,
                header: { 'Accept': 'text/event-stream' }
            })
            if (!res.body) {
                toast.error("오류가 발생했습니다. 다시 시도해주세요.", {
                    style: {
                        backgroundColor: "#FFB6C1",
                        color: "#000000"
                    }
                });
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
            toast.success("처리가 완료되었습니다.", {
                style: {
                    backgroundColor: "#D1FAE5",
                    color: "#000000"
                }
            });
        } catch (err) {
            console.error(err);
        }
    }


    return <Button onClick={() => {
        initResult()
        sendRequest(buildPayload(code1, lang1, code2, lang2, repeatCount, blocks))
    }}>제출</Button>
}

const buildPayload = (code1: string, lang1: string, code2: string, lang2: string, repeatCount: number, blocks: BlockSpec[]) => {
    return {
        TestcaseFormat: {
            variable_format: [],
            lines: convertKeysToSnakeCase(blocks.slice(1, blocks.length))
        },
        Code1: code1,
        Code1Language: lang1,
        Code2: code2,
        Code2Language: lang2,
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

const toSnakeCase = (str: string) => {
    return str.replace(/([A-Z])/g, "_$1").toLowerCase();
}

const convertKeysToSnakeCase = (obj: unknown): unknown => {
    if (Array.isArray(obj)) {
        return obj.map(convertKeysToSnakeCase);
    } else if (obj !== null && typeof obj === 'object') {
        return Object.fromEntries(
          Object.entries(obj).map(([key, value]) => [
              toSnakeCase(key),
              convertKeysToSnakeCase(value),
          ])
        );
    }
    return obj;
}

export default SubmitTestcaseRequestButton;