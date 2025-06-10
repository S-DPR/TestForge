export type CodeEditorProps = {
  code: string,
  language: string,
  setLang: (val: 'python') => void
  setCode: (val: string) => void
}