import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
} from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import {useState} from "react";

interface RegisterFormProps {
  setIsRenderLogin: (isRenderLogin: boolean) => void;
}

const RegisterForm = ({ setIsRenderLogin }: RegisterFormProps) => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [passwordConfirm, setPasswordConfirm] = useState("");

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

const register = async (email: string, password: string) => {
  const res = await fetch('http://localhost:9000/api/account/register/', {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email, password }),
    credentials: "include",
  })
  const data = await res.json()
  if (res.status >= 400) {
    console.log('register failed' + data.message);
    return;
  }
  console.log('register success');
}

export default RegisterForm;
