import React from 'react';
import './Footer.css'; 

const Footer = () => {
    return (
        <footer className="footer">
            <div className="footer-content">
                <p>{new Date().getFullYear()} Phishing Detection Project
                    Developed as a Computer Science Mini Project
                    by Arshin A S and Dinesh Kumar A S</p>
                
            </div>
        </footer>
    );
};

export default Footer;