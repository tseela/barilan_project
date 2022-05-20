import React from "react";
import './Navbar.css';
import { ImAirplane } from 'react-icons/im';
import { useToken } from '../../hooks';

export default function Navbar() {
    const { token, setToken } = useToken();
    var log_text = "login"
    if (token) {
        log_text = "logout";
    }

    return (
        <nav className="navbar container">
            <div className="logo">
                <ImAirplane className='logo-icon' size={33} />
                <p className="logo-text">
                <span>T</span>rip<span>P</span>lanner
                </p>
            </div>
            <menu>
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
                <li>
                    <a href="/login">{log_text}</a>
                </li>
                </ul>
            </menu>
        </nav>
    )
}

