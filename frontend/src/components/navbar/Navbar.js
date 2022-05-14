import React from "react";
import './Navbar.css';
import { ImAirplane } from 'react-icons/im';

export default function Navbar() {
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
                    <a href="/login">Login / Sign Up</a>
                </li>
                </ul>
            </menu>
        </nav>
    )
}

