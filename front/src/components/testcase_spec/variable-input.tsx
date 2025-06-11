"use client";

import { Popover, PopoverContent, PopoverTrigger } from "../ui/popover";
import { Button } from "../ui/button";
import {Command, CommandEmpty, CommandGroup, CommandInput, CommandItem} from "../ui/command";
import {useContext, useState} from "react";
import {TestcaseContext} from "@/context/TestcaseContext";

export interface VariableInputSpec {
    blockIndex: number;
    variableIndex: number;
    onChange?: (value: string) => void;
}

const VariableInput = ({ blockIndex, variableIndex, onChange }: VariableInputSpec) => {
    const ctx = useContext(TestcaseContext);
    if (!ctx) throw new Error("context 없음. 개판임 ㅠ");

    const { variables } = ctx;

    const [open, setOpen] = useState(false)
    const [value, setValue] = useState<string>("")

    const usableVariables = []
    for (let innerBlockIdx = 0; innerBlockIdx <= blockIndex; innerBlockIdx++) {
        for (let innerVariableIdx = 0; innerVariableIdx < variables[innerBlockIdx].length; innerVariableIdx++) {
            if (innerBlockIdx === blockIndex && innerVariableIdx > variableIndex) {
                break;
            }
            if (variables[innerBlockIdx][innerVariableIdx].name === '') {
                continue;
            }
            if (variables[innerBlockIdx][innerVariableIdx].type === 'char') {
                continue;
            }
            usableVariables.push(variables[innerBlockIdx][innerVariableIdx]);
        }
    }

    const handleSelect = (val: string) => {
        setValue(val)
        setOpen(false)
        onChange?.(val)
    }

    return (
        <Popover open={open} onOpenChange={setOpen}>
            <PopoverTrigger asChild>
                <Button variant="outline" className="w-[280px] justify-start">
                    {value || "값 선택 또는 입력"}
                </Button>
            </PopoverTrigger>
            <PopoverContent className="w-[280px] p-0 bg-white border border-gray-700">
                <Command>
                    <CommandInput
                        placeholder="변수 선택 혹은 입력"
                        onValueChange={setValue}
                        onKeyDown={(e) => {
                            if (e.key === "Enter") {
                                e.preventDefault()
                                if (value.trim() !== "") {
                                    handleSelect(value)
                                }
                            }
                        }}
                    />
                    <CommandGroup heading="사용 가능 변수">
                        {usableVariables.map((v, idx) => {
                            const name = `$${v.name}`
                            return (
                                <CommandItem
                                    key={idx}
                                    onSelect={() => handleSelect(name)}
                                >
                                    {name}
                                </CommandItem>
                            )
                        })}
                    </CommandGroup>
                    <CommandEmpty>결과 없음. Enter로 직접 입력 가능</CommandEmpty>
                </Command>
            </PopoverContent>
        </Popover>
    )
}

export default VariableInput;