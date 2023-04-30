import { createContext, useState, useEffect } from "react";
import jwt_decode from "jwt-decode";
import { useHistory } from "react-router-dom";
import { io } from 'socket.io-client';
const API_URL = process.env.REACT_APP_API_URL;


const AuthContext = createContext();

export default AuthContext;

export const AuthProvider = ({ children }) => {
  const history = useHistory();
  const Token = localStorage.getItem("authTokens")
  const verifyToken = async () => {
    const access_token = JSON.parse(Token).access_token
    const response = await fetch(`${API_URL}/auth/verify/`, {
      method: "POST",
      headers: {
        'Accept': 'application/json',
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        access_token
    })
    });
    const data = await response.json();
    if (response.status === 200) {
      
    } else {
      refreshToken();
    }
  };

  const refreshToken = async () => {
    const refresh_token = JSON.parse(Token).refresh_token
    const res = await fetch(`${API_URL}/auth/refresh/`, {
      method: 'POST',
      headers: {
          'Accept': 'application/json',
          'Authorization': `Bearer ${refresh_token}`
      }
    });
  const data = await res.json();
  if (res.status === 200) {
    localStorage.setItem("authTokens", JSON.stringify(data));
    setAuthTokens(data);
  } else {
    logoutUser();
  }

  }


  if (Token) {
    verifyToken();
  }


  const [authTokens, setAuthTokens] = useState(() =>
      Token
      ? JSON.parse(Token)
      : null
  );
  const [user, setUser] = useState(() =>
      Token
      ? jwt_decode(Token)
      : null
  );

  const socket = io(process.env.REACT_APP_API_URL, {
    path: process.env.REACT_APP_SOCKET_PATH,
    auth: (cb) => {
      cb(authTokens ? authTokens.access_token : null);
    },
  });

  const [loading, setLoading] = useState(true);


  const loginUser = async (username, password) => {
    const response = await fetch(`${API_URL}/auth/token/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        username,
        password
      })
    });
    const data = await response.json();

    if (response.status === 200) {
      setAuthTokens(data);
      setUser(jwt_decode(data.access_token));
      localStorage.setItem("authTokens", JSON.stringify(data));
      history.push("/");
      socket.emit('add_user', jwt_decode(data.access_token).sub)
    } else {
      return data;
    }
  };
  
  const registerUser = async (username, email, password) => {
    const response = await fetch(`${API_URL}/auth/register/`, {
      method: "POST",
      headers: {
        'Accept': 'application/json',
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        username,
        email,
        password
    })
    });
    if (response.status === 201) {
      history.push("/login");
    } else {
      alert("Something went wrong!");
    }
  };

  const logoutUser = () => {
    setAuthTokens(null);
    setUser(null);
    localStorage.removeItem("authTokens");
    history.push("/login");
  };




  const contextData = {
    user,
    socket,
    setUser,
    authTokens,
    setAuthTokens,
    registerUser,
    loginUser,
    logoutUser
  };

  useEffect(() => {
    if (authTokens) {
      setUser(jwt_decode(authTokens.access_token));
    }
    setLoading(false);
  }, [authTokens, loading]);

  return (
    <AuthContext.Provider value={contextData}>
      {loading ? null : children}
    </AuthContext.Provider>
  );
};