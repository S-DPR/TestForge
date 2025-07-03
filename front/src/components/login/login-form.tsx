import {Button} from "@/components/ui/button"
import {Card, CardContent, CardDescription, CardHeader,} from "@/components/ui/card"
import {Input} from "@/components/ui/input"
import {Label} from "@/components/ui/label"
import {useContext, useState} from "react";
import {toast} from "sonner";
import {HTTP_METHOD, LoginContext} from "@/context/LoginContext";

interface LoginFormProps {
  setIsRenderLogin: (isRenderLogin: boolean) => void;
  setLoginModalOpen: (isOpen: boolean) => void;
}

const LoginForm = ({ setIsRenderLogin, setLoginModalOpen }: LoginFormProps) => {
  const ctx = useContext(LoginContext);
  if (!ctx) throw new Error("또또또 콘텍스트 에러야");
  const { request, updateToken } = ctx;

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const login = async (email: string, password: string) => {
    const res = await request({
      url: 'http://localhost:9000/account/login/',
      method: HTTP_METHOD.POST,
      body: { email, password }
    });
    const data = await res.json();
    if (!data || !data.access) {
      setError("아이디 또는 비밀번호가 다릅니다.");
      return;
    }
    setError("");
    setLoginModalOpen(false);
    updateToken(data.access);
    toast.success("로그인 성공!", {
      style: {
        backgroundColor: "#D1FAE5",
        color: "#000000"
      }
    })
  }

  return (
    <div className={"flex flex-col gap-6"}>
      <Card>
        <CardHeader>
          <CardDescription>
            이메일과 비밀번호를 입력해주세요.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={(e) => {
            e.preventDefault();
            login(email, password);
          }}>
            <div className="flex flex-col gap-6">
              <div className="grid gap-3">
                <Label htmlFor="email">Email</Label>
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
                  <Label htmlFor="password">Password</Label>
                  <a
                    href="#"
                    className="ml-auto inline-block text-sm underline-offset-4 hover:underline"
                  >
                    Forgot your password?
                  </a>
                </div>
                <Input id="password" type="password" onChange={(e) => setPassword(e.target.value)} required />
              </div>
              {error && (
                  <div className="text-red-500 text-sm font-semibold">
                    {error} {/* 3. 에러 메시지 표시 */}
                  </div>
              )}
              <div className="flex flex-col gap-3">
                <Button type="submit" className="w-full">
                  Login
                </Button>
                <Button variant="outline" className="w-full">
                  Login with Google
                </Button>
              </div>
            </div>
            <div className="mt-4 text-center text-sm">
              계정이 없으신가요?{" "}
              <a href="#" className="underline underline-offset-4" onClick={() => setIsRenderLogin(false)}>
                회원가입
              </a>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}

export default LoginForm;
