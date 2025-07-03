import React, {createContext, ReactNode, useState} from "react";
import {toast} from "sonner";

interface LoginContextType {
  loginModalOpen: boolean;
  setLoginModalOpen: (open: boolean) => void;
  isRenderLogin: boolean;
  setIsRenderLogin: (open: boolean) => void;
  setAccessToken: (accessToken: string) => void;
  setExpiresAt: (expiresAt: number) => void;

  updateToken: (accessToken: string) => void;
  hasToken: () => boolean;
  logout: () => void;
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
  const [expiresAt, setExpiresAt] = useState(Number.MAX_SAFE_INTEGER);

  const request = async ({ url, method, body = {}, header = {} }: RequestType) => {
    const finalHeader = {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${accessToken}`,
      ...header,
    }

    if (Math.floor(Date.now() / 1000) >= expiresAt) {
      const res = await fetch('http://localhost:9000/refresh/', {
        method: HTTP_METHOD.POST,
        headers: finalHeader,
        credentials: 'include',
      })
      const data = await res.json();
      updateToken(data.access);
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

  const updateToken = (accessToken: string) => {
    console.log(atob(accessToken.split('.')[1]));
    const payload = JSON.parse(atob(accessToken.split('.')[1]));
    setAccessToken(accessToken);
    setExpiresAt(payload.exp);
  }

  const hasToken = () => {
    return accessToken.length > 0;
  }

  const logout = async () => {
    const res = await request({
      url: 'http://localhost:9000/account/logout/',
      method: HTTP_METHOD.POST,
    })
    const data = await res.json();
    if (!data.message) {
      toast.error('로그아웃에 실패했습니다.', {
        style: {
          backgroundColor: "#FFB6C1",
          color: "#000000"
        }
      });
      return;
    }
    setAccessToken("");
    setExpiresAt(Number.MAX_SAFE_INTEGER);
    toast.error("로그아웃에 성공했습니다.", {
      style: {
        backgroundColor: "#D1FAE5",
        color: "#000000"
      }
    });
  }

  return (<LoginContext.Provider value={{ loginModalOpen, setLoginModalOpen, isRenderLogin, setIsRenderLogin, setAccessToken, setExpiresAt, updateToken, hasToken, logout, request }}>
      {children}
    </LoginContext.Provider>
  );
}

export default LoginProvider;
