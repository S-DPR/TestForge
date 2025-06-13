import React, {createContext, ReactNode} from "react";

interface LoginContextType {
  loginOpen: boolean;
  setLoginOpen: (open: boolean) => void;
}

export const LoginContext = createContext<LoginContextType | null>(null);

const LoginProvider = ({ children }: { children: ReactNode }) => {
  const [loginOpen, setLoginOpen] = React.useState(false);

  return (<LoginContext.Provider value={{ loginOpen, setLoginOpen }}>
      {children}
    </LoginContext.Provider>
  );
}

export default LoginProvider;
