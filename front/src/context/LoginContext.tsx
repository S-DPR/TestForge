import React, {createContext, ReactNode} from "react";
import {toast} from "sonner";

interface LoginContextType {
  loginModalOpen: boolean;
  setLoginModalOpen: (open: boolean) => void;
  isRenderLogin: boolean;
  setIsRenderLogin: (open: boolean) => void;
  setAccessToken: (accessToken: string) => void;

  request: ({ url, method, body, header }: RequestType) => Promise<Response>;
}

interface RequestType {
  url: string;
  method: HTTP_METHOD;
  body?: object;
  header?: object;
}

export enum HTTP_METHOD {
  GET = 'GET',
  POST = 'POST',
  PUT = 'PUT',
  DELETE = 'DELETE',
  PATCH = 'PATCH',
}

export const LoginContext = createContext<LoginContextType | null>(null);

const LoginProvider = ({ children }: { children: ReactNode }) => {
  const [loginModalOpen, setLoginModalOpen] = React.useState(false);
  const [isRenderLogin, setIsRenderLogin] = React.useState(true);
  const [accessToken, setAccessToken] = React.useState("");

  const request = async ({ url, method, body = {}, header = {} }: RequestType) => {
    const finalHeader = {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${accessToken}`,
      ...header,
    }
    const response = await fetch(url, {
      method: method,
      headers: finalHeader,
      body: JSON.stringify(body),
      credentials: "include",
    })
    if (response.status === 401) {
      toast.error("로그인이 필요합니다.", {
        style: {
          backgroundColor: "#FFB6C1",
          color: "#000000"
        }
      });
      return response;
    }
    if (!(200 <= response.status && response.status < 300)) {
      toast.error("오류가 발생했습니다. 다시 시도해주세요.", {
        style: {
          backgroundColor: "#FFB6C1",
          color: "#000000"
        }
      })
    }
    return response;
  }

  return (<LoginContext.Provider value={{ loginModalOpen, setLoginModalOpen, isRenderLogin, setIsRenderLogin, setAccessToken, request }}>
      {children}
    </LoginContext.Provider>
  );
}

export default LoginProvider;
