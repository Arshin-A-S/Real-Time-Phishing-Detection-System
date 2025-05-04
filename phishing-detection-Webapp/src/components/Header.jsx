import React from 'react';
import './Header.css';

function Header() {
    return (
        <div className="header-section" id="Header">
            <h1 className='logo'>Phishing Detection Website</h1>
            <nav className="navbar">
                <ul className="navbar-links">
                    <li><a href="#Hero">Home</a></li>
                    <li><a href="#URLInput">Scan URL</a></li>
                    <li><a href="#URLInput">Chrome Extension</a></li>
                    <li><a href="#">About</a></li>
                    <li><a href="#contact">Contact</a></li>
                </ul>
            </nav>
        </div>
    );
}

export default Header;