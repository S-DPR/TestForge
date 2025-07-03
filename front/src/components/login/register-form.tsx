import {cn} from "@/lib/utils"
import {Button} from "@/components/ui/button"
import {Card, CardContent, CardDescription, CardHeader,} from "@/components/ui/card"
import {Input} from "@/components/ui/input"
import {Label} from "@/components/ui/label"
import {useContext, useState} from "react";
import {toast} from "sonner";
import {HTTP_METHOD, LoginContext} from "@/context/LoginContext";

interface RegisterFormProps {
  setIsRenderLogin: (isRenderLogin: boolean) => void;
}

const RegisterForm = ({ setIsRenderLogin }: RegisterFormProps) => {
  const ctx = useContext(LoginContext);
  if (!ctx) throw new Error("또또또 콘텍스트 에러야");
  const { request } = ctx;

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [passwordConfirm, setPasswordConfirm] = useState("");

  const register = async (email: string, password: string) => {
    const res = await request({
      url: 'http://localhost:9000/account/register/',
      method: HTTP_METHOD.POST,
      body: { email, password },
    })
    const data = await res.json();
    if (res.status >= 400) {
      toast.success("회원가입에 실패했습니다. : " + data.email.join(", "), {
        style: {
          backgroundColor: "#FFB6C1",
          color: "#000000"
        }
      });
      return;
    }
    setIsRenderLogin(true);
    toast.success("회원가입 성공!", {
      style: {
        backgroundColor: "#D1FAE5",
        color: "#000000"
      }
    });
  }

  return (
    <div className={cn("flex flex-col gap-6")}>
      <Card>
        <CardHeader>
          <CardDescription>
            이메일과 비밀번호, 그리고 비밀번호를 다시 한 번 입력해주세요.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={(e) => {
            e.preventDefault();
            register(email, password);
          }}>
            <div className="flex flex-col gap-6">
              <div className="grid gap-3">
                <Label htmlFor="email">이메일</Label>
                <Input
                  id="email"
                  type="email"
                  placeholder="m@example.com"
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />
              </div>
              <div className="grid gap-3">
                <div className="flex items-center">
                  <Label htmlFor="password">비밀번호</Label>
                </div>
                <Input id="password" type="password" onChange={(e) => setPassword(e.target.value)} required />
              </div>

              <div className="grid gap-3">
                <div className="flex items-center">
                  <Label htmlFor="password">비밀번호 확인</Label>
                </div>
                <Input id="passwordConfirm" type="password" onChange={(e) => setPasswordConfirm(e.target.value)} required />
              </div>
              <div className="flex flex-col gap-3">
                <Button type="submit" className="w-full" disabled={!email || password != passwordConfirm}>
                  회원가입
                </Button>
              </div>
            </div>
            <div className="mt-4 text-center text-sm">
              계정이 있으신가요?{" "}
              <a href="#" className="underline underline-offset-4" onClick={() => setIsRenderLogin(true)}>
                로그인
              </a>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}

export default RegisterForm;
