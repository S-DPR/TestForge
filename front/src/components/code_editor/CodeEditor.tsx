'use client'

import React from 'react'
import CodeMirror from '@uiw/react-codemirror'
import { python } from '@codemirror/lang-python'

import {
  Select,
  SelectTrigger,
  SelectValue,
  SelectContent,
  SelectGroup,
  SelectLabel,
  SelectItem,
} from '@/components/ui/select'
import {CodeEditorProps} from "@/components/code_editor/codeEditorTypes";

const extensionsMap: Record<string, () => import('@codemirror/state').Extension> = {
  python,
}

const CodeEditor = (codeEditorProps: CodeEditorProps) => {
  return (
    <div className="space-y-4">
      <Select value={codeEditorProps.language} onValueChange={(val: 'python') => codeEditorProps.setLang(val)}>
        <SelectTrigger className="w-[180px] border-gray-600 rounded-md px-3 py-2">
          <SelectValue placeholder="언어 선택" />
        </SelectTrigger>
        <SelectContent className="bg-white border border-gray-700">
          <SelectGroup>
            <SelectLabel>언어</SelectLabel>
            <SelectItem value="python">Python</SelectItem>
          </SelectGroup>
        </SelectContent>
      </Select>

      <CodeMirror
        value={codeEditorProps.code}
        height="300px"
        extensions={[extensionsMap[codeEditorProps.language]()]}
        onChange={(val) => codeEditorProps.setCode(val)}
        theme="dark"
      />
    </div>
  )
}

export default CodeEditor
