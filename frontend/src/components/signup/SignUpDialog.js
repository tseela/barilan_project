import React, { useState } from 'react';
import PropTypes from 'prop-types';
import './SignUpDialog.css';

async function signUser(credentials) {
  let res = await fetch('/signup', {
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

export default function SignUpDialog({ setToken }) {
  const [username, setUserName] = useState();
  const [password, setPassword] = useState();
  const [confirm_password, setConfirmPassword] = useState();

  const handleSubmit = async e => {
    e.preventDefault();

    if (username === '' || password === '') {
      alert("REGISTRATION FAILED: Username and password must not be empty.");
      return;
    }

    if (confirm_password !== password) {
      alert("REGISTRATION FAILED: Confirm Password and Password doesn't match.");
      return;
    }

    const token = await signUser({
      'username' : username,
      'password' : password,
    });

    if (token) {
      setToken(token);
    } else {
      alert("REGISTRATION FAILED: This username is taken. Choose a different one.");
    }
  }

  return(
    <div className="signup-wrapper">
      <h className="headline" >Sign Up</h>
      <form onSubmit={handleSubmit}>
        <label>
          <input className='form' type="text" placeholder="Username" onChange={e => setUserName(e.target.value)} />
        </label>
        <p></p>
        <label>
          <input className='form' type="password" placeholder="Password" onChange={e => setPassword(e.target.value)} />
        </label>
        <br></br>
        <label>
          <input className='form conf-pass' type="password" placeholder="Confirm Password" onChange={e => setConfirmPassword(e.target.value)} />
        </label>
        <div className='signup-btn-div'>
          <button className='signup-btn' type="submit">Sign Up</button>
        </div>
      </form>
      <div className='go-login'>
        You already have an account? <a href='/login'>Login</a>
      </div>
    </div>
  )
}

SignUpDialog.propTypes = {
  setToken: PropTypes.func.isRequired
}
