import {Input} from "@/components/ui/input";
import React from "react";

interface DefineRangeSpec {
  min: number;
  max: number;
}

const DefineRange = ({ min, max }: DefineRangeSpec) => {
  return (
    <div>
      <Input placeholder={"min"} defaultValue={min}></Input>
      <Input placeholder={"max"} defaultValue={max}></Input>
    </div>
  )
}

export default DefineRange
