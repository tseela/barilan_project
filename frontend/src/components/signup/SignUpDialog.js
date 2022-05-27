import React, { useState } from 'react';
import PropTypes from 'prop-types';
import './SignUpDialog.css';

async function signUser(credentials) {
 return fetch('/signup', {
   method: 'POST',
   headers: {
     'Content-Type': 'application/json'
   },
   body: JSON.stringify(credentials)
 })
   .then(data => data.json())
}

export default function SignUpDialog({ setToken }) {
  const [username, setUserName] = useState();
  const [password, setPassword] = useState();
  const [confirm_password, setConfirmPassword] = useState();

  const handleSubmit = async e => {
    e.preventDefault();
    if (confirm_password !== password) {
      alert("Confirm Password and Password doesn't match.");
      return;
    }
    const token = await signUser({
      'username' : username,
      'password' : password,
    });
    setToken(token);
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
