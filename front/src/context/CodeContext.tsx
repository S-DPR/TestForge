import React, {createContext, ReactNode} from "react";

interface CodeContextType {
    code1: string;
    lang1: string;

    code2: string;
    lang2: string;

    setCode1: (code1: string) => void;
    setLang1: (lang1: 'python' | 'cpp' | 'java') => void;

    setCode2: (code2: string) => void;
    setLang2: (lang2: 'python' | 'cpp' | 'java') => void;

    repeatCount: number;
    setRepeatCount: (repeatCount: number) => void;
}

export const CodeContext = createContext<CodeContextType | null>(null);

const CodeProvider = ({ children }: { children: ReactNode }) => {
    const [code1, setCode1] = React.useState('');
    const [lang1, setLang1] = React.useState<'python' | 'cpp' | 'java'>('python');

    const [code2, setCode2] = React.useState('');
    const [lang2, setLang2] = React.useState<'python' | 'cpp' | 'java'>('python');

    const [repeatCount, setRepeatCount] = React.useState(1);

    return (<CodeContext.Provider value={{ code1, setCode1, lang1, setLang1, code2, setCode2, lang2, setLang2, repeatCount, setRepeatCount }}>
        {children}
    </CodeContext.Provider>
    );
}

export default CodeProvider;
