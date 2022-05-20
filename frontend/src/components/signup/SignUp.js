import React, { useState } from 'react';
import PropTypes from 'prop-types';
import './SignUp.css';

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

export default function SignUp({ setToken }) {
  const [username, setUserName] = useState();
  const [password, setPassword] = useState();

  const handleSubmit = async e => {
    e.preventDefault();
    const token = await signUser({
      'username' : username,
      'password' : password,
    });
    setToken(token);
  }

  return(
    <div className="signup-wrapper">
      <h1>Please Sign Up</h1>
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

SignUp.propTypes = {
  setToken: PropTypes.func.isRequired
}
