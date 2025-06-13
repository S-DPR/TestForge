import {useContext} from "react";
import {LoginContext} from "@/context/LoginContext";

const LoginButton = () => {
  const ctx = useContext(LoginContext);
  if (!ctx) throw new Error("LoginContext undefined");

  const { setLoginOpen } = ctx;

  return (
    <div className="flex justify-start">
      <button
        onClick={() => setLoginOpen(true)}
        className="text-sm text-muted-foreground hover:underline"
      >
        로그인
      </button>
    </div>
  );
}

export default LoginButton;
