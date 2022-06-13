import { useState } from 'react';

// retrive from storage
function getToken() {
  return JSON.parse(sessionStorage.getItem('token'))?.token;
}

// useToken hook to store token in session storage
export default function useToken() {
  const [token, setToken] = useState(getToken());

  // update in both storage and state var
  const updateToken = userToken => {
    sessionStorage.setItem('token', JSON.stringify(userToken));
    setToken(userToken?.token);
  };

  return {
    setToken: updateToken,
    token
  }
}
