import React from "react";
import './Navbar.css';
import { ImAirplane } from 'react-icons/im';
import { useToken } from '../../hooks';

export default function Navbar() {
    const { token, setToken } = useToken();

    const logout = async e => {
        setToken(null);
    }

    var link = <a href="/login">Login</a>; //login
    if (token) { // logout // may need to change that one
        link = <div className="logout-div">{token.user}
        <a href="/login" id="logout" onClick={logout}>Logout</a>
        </div>;
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
                    <a href="/trip_planning">Trip Planning</a>
                </li>
                <li>
                    <a href="/profile">My Profile</a>
                </li>
                <li className="login-link">
                    {link}
                </li>
                </ul>
            </menu>
        </nav>
    )
}

