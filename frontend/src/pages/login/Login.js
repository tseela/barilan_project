import React, { useState } from 'react';
import { useToken } from '../../hooks';
import './Login.css';

async function loginUser(credentials) {
 return fetch('/signup', {
   method: 'POST',
   headers: {
     'Content-Type': 'application/json'
   },
   body: JSON.stringify(credentials)
 })
   .then(data => data.json())
}

export default function Login() {
  const [username, setUserName] = useState();
  const [password, setPassword] = useState();
  const { token, setToken } = useToken();

  if (token) {
    return(
      <div>
        <button onClick={() => setToken(null)}>Logout from account</button>
      </div>
    )
  }

  const handleSubmit = async e => {
    e.preventDefault();
    const token = await loginUser({
      'username' : username,
      'password' : password,
    });
    setToken(token);
  }

  return(
    <div className="login-wrapper">
      <h1>Please Log In</h1>
      <form onSubmit={handleSubmit}>
        <label>
          <p>Username</p>
          <input type="text" onChange={e => setUserName(e.target.value)} />
        </label>
        <label>
          <p>Password</p>
          <input type="password" onChange={e => setPassword(e.target.value)} />
        </label>
        <div>
          <button type="submit">Submit</button>
        </div>
      </form>
    </div>
  )
}
