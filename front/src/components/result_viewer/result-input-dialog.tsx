import {useContext} from "react";
import {
  Dialog,
  DialogContent, DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import {ResultContext} from "@/context/ResultContext";

const ResultInputDialog = () => {
  const ctx = useContext(ResultContext);
  if (!ctx) throw new Error("Can't find result context");

  const { inputSelected, inputDialogOpen, setInputDialogOpen } = ctx;

  return (
    <Dialog open={inputDialogOpen} onOpenChange={setInputDialogOpen}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>입력값</DialogTitle>
          <DialogDescription>선택한 항목에 대한 입력값입니다.</DialogDescription>
        </DialogHeader>
        <div className="mt-4 font-mono text-sm whitespace-pre-wrap max-h-[60vh] overflow-y-auto">
          {inputSelected ?? "입력을 찾을 수 없습니다."}
        </div>
      </DialogContent>
    </Dialog>
  );
};

export default ResultInputDialog;
