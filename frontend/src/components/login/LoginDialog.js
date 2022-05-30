import React, { useState } from 'react';
import PropTypes from 'prop-types';
import './LoginDialog.css';

async function loginUser(credentials) {
  return fetch('/signup', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(credentials)
  }).then(data => data.json())
}

export default function LoginDialog({ setToken }) {
  const [username, setUserName] = useState();
  const [password, setPassword] = useState();

  const handleSubmit = async e => {
    e.preventDefault();
    const token = await loginUser({
      'username' : username,
      'password' : password,
    });
    if (token) {
      setToken(token);
    }
    // error login
  }

  return(
    <div className="login-wrapper">
      <h className="headline" >Log In</h>
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
