import { useState } from 'react';

function getToken() {
  return JSON.parse(sessionStorage.getItem('token'))?.token;
}

export default function useToken() {
  const [token, setToken] = useState(getToken());

  const updateToken = userToken => {
    sessionStorage.setItem('token', JSON.stringify(userToken));
    setToken(userToken?.token);
  };

  return {
    setToken: updateToken,
    token
  }
}
