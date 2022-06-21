import React from "react";
import './Navbar.css';
import { ImAirplane } from 'react-icons/im';
import { useToken } from '../../hooks';

// app navbar
export default function Navbar() {
    const { token, setToken } = useToken();

    const logout = async e => {
        setToken(null);
    }

    // last link in navbar will be login/logout depends of token state
    // profile link won't be pressable if user is not connected
    var link = <a href="/login">Login</a>; //login
    var profile = <div className="profile-div">My Profile</div> // not pressable
    if (token) { // user connected
        link = <div className="logout-div">{token.user}
        <a href="/login" id="logout" onClick={logout}>Logout</a>
        </div>; // logout
        profile = <a href="/profile">My Profile</a>; // pressable
    }

    return (
        <nav className="navbar-container">
            <div className="logo">
                <ImAirplane className='logo-icon' />
                <p className="logo-text">
                <span>T</span>rip<span>P</span>lanner
                </p>
            </div>
            <menu className="nav-menu">
                <ul className="nav-links">
                <li>
                    <a href="/home">Home</a>
                </li>
                <li>
                    <a href="/plantrip">Trip Planning</a>
                </li>
                <li>
                    {profile}
                </li>
                <li className="login-link">
                    {link}
                </li>
                </ul>
            </menu>
        </nav>
    )
}

