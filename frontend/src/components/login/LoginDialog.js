import React, { useState } from 'react';
import PropTypes from 'prop-types';
import './LoginDialog.css';

async function loginUser(credentials) {
  let res = await fetch('/signin', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(credentials)
  });

  if (res.status !== 200) {
    return null;
  }
  
  let ret = res.json();
  return ret;
}

export default function LoginDialog({ setToken }) {
  const [username, setUserName] = useState();
  const [password, setPassword] = useState();

  const handleSubmit = async e => {
    e.preventDefault();

    if (username === '' || password === '') {
      alert("LOGIN FAILED: Username and password must not be empty.");
      return;
    }

    const token = await loginUser({
      'username' : username,
      'password' : password,
    });
    
    if (token) {
      setToken(token);
    } else {
      alert("LOGIN FAILED: Username or Password are incorrect.");
    }
  }

  return(
    <div className="login-wrapper">
      <header className="headline" >Log In</header>
      <form onSubmit={handleSubmit}>
        <label>
          <input className='form' type="text" placeholder="Username" onChange={e => setUserName(e.target.value)} />
        </label>
        <p></p>
        <label>
          <input className='form' type="password" placeholder="Password" onChange={e => setPassword(e.target.value)} />
        </label>
        <div className='login-btn-div'>
          <button className='login-btn' type="submit">Login</button>
        </div>
      </form>
      <div className='go-register'>
        You don't have an account? <a href='/signup'>Register</a>
      </div>
    </div>
  )
}

LoginDialog.propTypes = {
  setToken: PropTypes.func.isRequired
}
