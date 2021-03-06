import React from "react";
import './Navbar.css';
import { ImAirplane } from 'react-icons/im';
import { useToken } from '../../hooks';

/**
 * navbar for app
 * 
 * @returns 
 */
export default function Navbar() {
    const { token, setToken } = useToken(); // user token

    // logout
    function logout() {
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
            {/* website logo */}
            <div className="logo">
                <ImAirplane className='logo-icon' />
                <p className="logo-text">
                <span>T</span>rip<span>P</span>lanner
                </p>
            </div>
            {/* nav menu */}
            <menu className="nav-menu">
                <ul className="nav-links">
                <li>
                    <a href="/home">Home</a>
                </li>
                <li>
                    <a href='/tripplanning'>Trip Planning</a>
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

