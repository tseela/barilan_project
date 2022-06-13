import React, { useState } from 'react';
import PropTypes from 'prop-types';
import './SignUpDialog.css';

// request server to sign up user
async function signUser(credentials) {
  let res = await fetch('/signup', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(credentials)
  });
  
  let ret = res.json();
  return ret;
}

export default function SignUpDialog() {
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

    const res = await signUser({
      'username' : username,
      'password' : password,
    });

    alert(res?.message); // alert user about registration state
  }

  return(
    <div className="signup-wrapper">
      <header className="headline" >Sign Up</header>
      <form onSubmit={handleSubmit}>
        <label>
          <input className='form' type="text" placeholder="Username" maxLength="10" onChange={e => setUserName(e.target.value)} />
        </label>
        <p></p>
        <label>
          <input className='form' type="password" placeholder="Password" maxLength="18" onChange={e => setPassword(e.target.value)} />
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
