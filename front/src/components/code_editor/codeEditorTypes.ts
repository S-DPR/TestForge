export type CodeEditorProps = {
  code: string,
  language: string,
  setLang: (val: 'python' | 'cpp' | 'java') => void
  setCode: (val: string) => void
}