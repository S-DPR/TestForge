import {useContext} from "react";
import {LoginContext} from "@/context/LoginContext";

const LoginButton = () => {
  const ctx = useContext(LoginContext);
  if (!ctx) throw new Error("LoginContext undefined");

  const { hasToken, logout, setLoginModalOpen } = ctx;

  return (
    <div className="flex justify-start">
      {
        hasToken() ?
          <button
            onClick={() => logout()}
            className="text-sm text-muted-foreground hover:underline"
          >로그아웃</button> :
          <button
            onClick={() => setLoginModalOpen(true)}
            className="text-sm text-muted-foreground hover:underline"
          >로그인</button>
      }
    </div>
  );
}

export default LoginButton;
