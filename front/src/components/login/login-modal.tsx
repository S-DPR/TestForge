import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import LoginForm from "@/components/login/login-form";
import {useContext} from "react";
import {LoginContext} from "@/context/LoginContext";

const LoginModal = () => {
  const ctx = useContext(LoginContext);
  if (!ctx) throw new Error("LoginContext undefined");

  const { loginOpen, setLoginOpen } = ctx;

  return (
    <Dialog open={loginOpen} onOpenChange={setLoginOpen}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle>로그인</DialogTitle>
        </DialogHeader>
        <LoginForm />
      </DialogContent>
    </Dialog>
  );
}

export default LoginModal;
