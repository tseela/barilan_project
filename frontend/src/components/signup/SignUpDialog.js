import React, { useRef, useState } from 'react';
import PropTypes from 'prop-types';
import './SignUpDialog.css';

/**
 * signup dialog box
 * 
 * @param setToken - sets the token (should update session storage too)
 * @param directToRegister - should add a link to register
 * @returns 
 */
export default function SignUpDialog({ alertSignUp, directToLogin=true }) {
  const [username, setUserName] = useState(); // name
  const [password, setPassword] = useState(); // pass
  const [confirm_password, setConfirmPassword] = useState(); // conf pass
  const formRef = useRef();

  // request server to sign up user
  async function signUser(credentials) {
    let res = await fetch('/signup', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(credentials)
    });

    if (res.status === 200) { // if ok, alert sign up is good
      setTimeout(() => {
        alertSignUp();
      }, 500);
    }
  
    let ret = res.json();
    return ret;
  }

  // on submit form sent
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

    formRef.current.reset(); // clear form
  }

  return(
    <div className="signup-wrapper">
      <header className="headline" >Sign Up</header>
      <form onSubmit={handleSubmit} ref={formRef}>
        {/* username */}
        <label>
          <input className='form' type="text" placeholder="Username" maxLength="10" onChange={e => setUserName(e.target.value)} />
        </label>
        <p></p>
        {/* pass */}
        <label>
          <input className='form' type="password" placeholder="Password" maxLength="18" onChange={e => setPassword(e.target.value)} />
        </label>
        <br></br>
        {/* conf pass */}
        <label>
          <input className='form conf-pass' type="password" placeholder="Confirm Password" onChange={e => setConfirmPassword(e.target.value)} />
        </label>
        {/* submit credentials button */}
        <div className='signup-btn-div'>
          <button className='signup-btn' type="submit">Sign Up</button>
        </div>
      </form>
      {/* directs to login if needed */}
      {directToLogin ? <div className='go-login'>
        You already have an account? <a href='/login'>Login</a>
      </div> : ''}
    </div>
  )
}

SignUpDialog.propTypes = {
  alertSignUp: PropTypes.func,
  directToLogin: PropTypes.bool
}
