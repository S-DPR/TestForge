import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import LoginForm from "@/components/login/login-form";
import {useContext} from "react";
import {LoginContext} from "@/context/LoginContext";
import RegisterForm from "@/components/login/register-form";

const LoginModal = () => {
  const ctx = useContext(LoginContext);
  if (!ctx) throw new Error("LoginContext undefined");

  const { loginModalOpen, setLoginModalOpen } = ctx;
  const { isRenderLogin, setIsRenderLogin } = ctx;

  return (
    <Dialog open={loginModalOpen} onOpenChange={setLoginModalOpen}>
      <DialogContent className="sm:max-w-md">
        {isRenderLogin ? (
          <>
            <DialogHeader>
              <DialogTitle>로그인</DialogTitle>
            </DialogHeader>
            <LoginForm setIsRenderLogin={setIsRenderLogin} />
          </>) : (
          <>
            <DialogHeader>
              <DialogTitle>회원가입</DialogTitle>
            </DialogHeader>
            <RegisterForm setIsRenderLogin={setIsRenderLogin} />
          </>
        )}
      </DialogContent>
    </Dialog>
  );
}

export default LoginModal;
