import React, {createContext, ReactNode} from "react";

interface LoginContextType {
  loginModalOpen: boolean;
  setLoginModalOpen: (open: boolean) => void;
  isRenderLogin: boolean;
  setIsRenderLogin: (open: boolean) => void;
}

export const LoginContext = createContext<LoginContextType | null>(null);

const LoginProvider = ({ children }: { children: ReactNode }) => {
  const [loginModalOpen, setLoginModalOpen] = React.useState(false);
  const [isRenderLogin, setIsRenderLogin] = React.useState(true);

  return (<LoginContext.Provider value={{ loginModalOpen, setLoginModalOpen, isRenderLogin, setIsRenderLogin }}>
      {children}
    </LoginContext.Provider>
  );
}

export default LoginProvider;
