import {Input} from "@/components/ui/input";
import React from "react";

interface DefineRangeSpec {
  min: number;
  max: number;
}

const DefineRange = ({ min, max }: DefineRangeSpec) => {
  return (
    <div>
      <Input placeholder={"min"} value={min}></Input>
      <Input placeholder={"max"} value={max}></Input>
    </div>
  )
}

export default DefineRange
