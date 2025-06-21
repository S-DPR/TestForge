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
    showChar: boolean;
    onChange: (value: string) => void;
    value: string;
}

const VariableInput = ({ blockIndex, variableIndex, isRenderReserved, showChar, onChange, value }: VariableInputSpec) => {
    const ctx = useContext(TestcaseContext);
    if (!ctx) throw new Error("context 없음. 개판임 ㅠ");

    const { blocks } = ctx;

    const [open, setOpen] = useState(false)

    if (!isRenderReserved) isRenderReserved = false;
    const reservedVariable = (type: string): Array<{ description: string, value: string }> => {
        switch (type) {
            case 'line':
                return [];
            case 'graph':
                return [
                    { description: '간선의 시작점', value: '$_s' },
                    { description: '간선의 끝점.', value: '$_e' },
                    { description: '간선의 가중치', value: '$_w' }
                ];
            case 'matrix': case 'string':
                return[
                    { description: '완성된 행렬을 담은 변수', value: '$_element' }
                ];
        }
        return [];
    }

    const commonConstants = [
        { description: '\'a\'의 아스키코드', value: '97' },
        { description: '\'z\'의 아스키코드', value: '122' },
        { description: '\'A\'의 아스키코드', value: '65' },
        { description: '\'Z\'의 아스키코드', value: '90' },
        { description: '\'0\'의 아스키코드', value: '48' },
        { description: '\'9\'의 아스키코드', value: '57' }
    ]

    const usableVariables = []
    for (let innerBlockIdx = 0; innerBlockIdx <= blockIndex; innerBlockIdx++) {
        for (let innerVariableIdx = 0; innerVariableIdx < blocks[innerBlockIdx].variable.length; innerVariableIdx++) {
            if (innerBlockIdx === blockIndex && innerVariableIdx > variableIndex-1) { // 현재 보는 variable index는 사용 불가능
                break;
            }
            if (!blocks[innerBlockIdx].variable[innerVariableIdx]) {
                continue;
            }
            if (blocks[innerBlockIdx].variable[innerVariableIdx].name === '') {
                continue;
            }
            if (!showChar && blocks[innerBlockIdx].variable[innerVariableIdx].type === 'char') {
                continue;
            }
            usableVariables.push(blocks[innerBlockIdx].variable[innerVariableIdx]);
        }
    }

    const blockTypes = [...new Set(blocks.slice(1, blockIndex+1).map(block => block.type))]

    const handleSelect = (val: string) => {
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
            <PopoverContent className="w-[280px] p-0 bg-white border border-gray-200 shadow-md rounded-md z-50 max-h-[300px] overflow-y-auto">
                <Command>
                    {!showChar && (
                      <CommandGroup
                        heading="이 설정은 char형식을 지원하지 않습니다."
                        className="px-3 py-2 text-xs text-muted-foreground"
                      />
                    )}
                    <CommandInput
                        placeholder="변수 선택 혹은 입력"
                        className="text-sm px-3 py-2 border-b border-gray-200"
                        onValueChange={(val) => {
                            onChange(val)
                        }}
                        onKeyDown={(e) => {
                            if (e.key === "Enter") {
                                e.preventDefault();
                                handleSelect(value);
                            }
                        }}
                    />
                    <CommandGroup heading="정의된 사용 가능 변수" className="px-3 py-2 text-xs text-muted-foreground">
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
                            {reservedVariable(type).map(({description, value}, varIdx) => (
                              <CommandItem key={`reserved-${varIdx}`} className="justify-between"  onSelect={() => handleSelect(value)}>
                                  {value}
                                  <span className="text-muted-foreground text-xs">{description}</span>
                              </CommandItem>
                            ))}
                        </CommandGroup>)
                    })}
                    <CommandGroup heading="공통 상수" className="px-3 py-2 text-xs text-muted-foreground">
                    {commonConstants.map(({description, value}, idx) => (
                            <CommandItem key={`common-constants-${idx}`} className="justify-between"  onSelect={() => handleSelect(value)}>
                                {value}
                                <span className="text-muted-foreground text-xs">{description}</span>
                            </CommandItem>
                        ))
                    }
                    </CommandGroup>
                    <CommandEmpty>결과 없음. Enter로 직접 입력 가능</CommandEmpty>
                </Command>
            </PopoverContent>
        </Popover>
    )
}

export default VariableInput;