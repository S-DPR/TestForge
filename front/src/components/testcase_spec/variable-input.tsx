"use client";

import { Popover, PopoverContent, PopoverTrigger } from "../ui/popover";
import { Button } from "../ui/button";
import {Command, CommandEmpty, CommandGroup, CommandInput, CommandItem} from "../ui/command";
import {useContext, useState} from "react";
import {TestcaseContext} from "@/context/TestcaseContext";

export interface VariableInputSpec {
    blockIndex: number;
    variableIndex: number;
    isRenderReserved?: boolean;
    onChange?: (value: string) => void;
    value: string;
    setValue?: (v: string) => void;
}

const VariableInput = ({ blockIndex, variableIndex, isRenderReserved, onChange, value, setValue }: VariableInputSpec) => {
    const ctx = useContext(TestcaseContext);
    if (!ctx) throw new Error("context 없음. 개판임 ㅠ");

    const { blocks } = ctx;

    const [open, setOpen] = useState(false)

    if (!isRenderReserved) isRenderReserved = false;
    if (!setValue) setValue = (_: string) => {}
    const reservedVariable: Record<string, Array<string>> = {
        'line': [],
        'graph': ['$_s', '$_e', '$_w'],
        'matrix': ['$_element']
    }

    const usableVariables = []
    for (let innerBlockIdx = 0; innerBlockIdx <= blockIndex; innerBlockIdx++) {
        for (let innerVariableIdx = 0; innerVariableIdx < blocks[innerBlockIdx].variables.length; innerVariableIdx++) {
            if (innerBlockIdx === blockIndex && innerVariableIdx > variableIndex-1) { // 현재 보는 variable index는 사용 불가능
                break;
            }
            if (!blocks[innerBlockIdx].variables[innerVariableIdx]) {
                continue;
            }
            if (blocks[innerBlockIdx].variables[innerVariableIdx].name === '') {
                continue;
            }
            if (blocks[innerBlockIdx].variables[innerVariableIdx].type === 'char') {
                continue;
            }
            usableVariables.push(blocks[innerBlockIdx].variables[innerVariableIdx]);
        }
    }

    const blockTypes = [...new Set(blocks.slice(1, blocks.length).map(block => block.type))]

    const handleSelect = (val: string) => {
        setValue(val)
        setOpen(false)
        onChange?.(val)
    }

    return (
        <Popover open={open} onOpenChange={setOpen}>
            <PopoverTrigger asChild>
                <Button variant="outline" className="w-[280px] justify-start text-sm text-gray-800 bg-white hover:bg-gray-50 border-gray-300">
                    {value || "값 선택 또는 입력"}
                </Button>
            </PopoverTrigger>
            <PopoverContent className="w-[280px] p-0 bg-white border border-gray-200 shadow-md rounded-md z-50">
                <Command>
                    <CommandInput
                        placeholder="변수 선택 혹은 입력"
                        className="text-sm px-3 py-2 border-b border-gray-200"
                        onValueChange={(val) => {
                            setValue(val)
                            handleSelect(val)
                        }}
                    />
                    <CommandGroup heading="사용 가능 변수" className="px-3 py-2 text-xs text-muted-foreground">
                        {usableVariables.map((v, idx) => {
                            const name = `$${v.name}`
                            return (
                                <CommandItem
                                    key={`variable-select-${blockIndex}-${variableIndex}-${idx}`}
                                    onSelect={() => handleSelect(name)}
                                >
                                    {name}
                                </CommandItem>
                            )
                        })}
                    </CommandGroup>
                    {isRenderReserved && blockTypes.map((type, idx) => {
                        return (<CommandGroup key={idx} heading={`${type} 예약 변수`} className="px-3 py-2 text-xs text-muted-foreground">
                            {reservedVariable[type].map((name, varIdx) => (
                              <CommandItem key={varIdx} onSelect={() => handleSelect(name)}>
                                  {name}
                              </CommandItem>)
                            )}
                        </CommandGroup>)
                    })}
                    <CommandEmpty>결과 없음. Enter로 직접 입력 가능</CommandEmpty>
                </Command>
            </PopoverContent>
        </Popover>
    )
}

export default VariableInput;