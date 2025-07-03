import {useContext} from "react";
import {Result, ResultContext} from "@/context/ResultContext";
import {clsx} from "clsx";
import {HTTP_METHOD, LoginContext} from "@/context/LoginContext";

const ResultBox = () => {
  const ctx = useContext(ResultContext);
  const loginCtx = useContext(LoginContext);

  if (!ctx) throw new Error("Can't find result context");
  if (!loginCtx) throw new Error("Can't find login context");

  const { results, setInputSelected, setInputDialogOpen } = ctx;
  const { request } = loginCtx;

  const handleClick = async (result: Result) => {
    const res = await request({
      url: `http://localhost:9001/file/${result.filename}`,
      method: HTTP_METHOD.GET,
    })
    const text = await res.text();
    const data = JSON.parse(text);
    setInputSelected(data.content);
    setInputDialogOpen(true);
  }

  return (
    <div className="grid grid-cols-5 gap-4">
      {results.map((result, idx) => (
        <div
          key={idx}
          className={clsx(
            "h-12 flex items-center justify-center font-semibold rounded-lg shadow-sm",
            "cursor-pointer hover:brightness-95 transition",
            getStatusClass(result.diffStatus)
          )}
          onClick={() => handleClick(result)}
        >
          {result.diffStatus}
        </div>
      ))}
    </div>
  );
}

const getStatusClass = (status: string) => {
  if (!status) return "bg-gray-100";
  if (status.includes("ERROR FAILED")) return "bg-red-500 text-white";
  if (status.includes("ERROR BUT EQUAL")) return "bg-yellow-200";
  if (status === "DIFFERENT") return "bg-red-100";
  if (status === "EQUAL") return "bg-green-200";
  return "bg-gray-100";
};

export default ResultBox;
