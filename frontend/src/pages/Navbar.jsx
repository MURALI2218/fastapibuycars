import React, { useState } from "react";
import { Link } from "react-router-dom";
import "./navbar.css";
import { ACCESS_TOKEN } from '../constant';


const Navbar = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  const closeMenu = () => {
    setIsMenuOpen(false);
  };


  const token = localStorage.getItem(ACCESS_TOKEN);
  
  
  return (
    <>
      <header className="header">
        <nav className="nav-container">
          {/* Extreme Left: Hamburger Toggle Button */}
          <button
            className={`hamburger-btn ${isMenuOpen ? "active" : ""}`}
            onClick={toggleMenu}
            aria-label="Toggle menu"
          >
            <span className="bar"></span>
            <span className="bar"></span>
            <span className="bar"></span>
          </button>

          {/* Brand Logo */}
          <h2 className="logo">
            <Link to="/" onClick={closeMenu}>
              Buy Cars
            </Link>
          </h2>

          {/* Desktop Links (Visible on large screens) */}
          <div className="nav-links desktop-only">
            <Link className="nav-btn" to="/">
              Home
            </Link>
            <Link className="nav-btn" to="/owncarslist">
              Your Cars
            </Link>
            <Link className="nav-btn" to="/profile">
              Profile
            </Link>
       
            {!token ? (
              <Link to="/login" className="nav-btn primary-btn">
                Login
              </Link>
            ) : (
              <Link to="/logout" className="nav-btn logout-btn">
                Logout
              </Link>
            )}
          </div>
        </nav>
      </header>

      {/* Slide-out Left Drawer Panel */}
      <div className={`drawer-menu ${isMenuOpen ? "open" : ""}`}>
        <div className="drawer-header">
          <h3>Menu</h3>
          <button className="close-btn" onClick={closeMenu} aria-label="Close menu">
            &times;
          </button>
        </div>

        <div className="drawer-links">
          <Link className="drawer-item" to="/" onClick={closeMenu}>
            Home
          </Link>
          <Link className="drawer-item" to="/owncarslist" onClick={closeMenu}>
            Your Cars
          </Link>
          <Link className="drawer-item" to="/profile" onClick={closeMenu}>
            Profile
          </Link>

          {!token ? (
            <Link
              to="/login"
              className="drawer-item primary-btn"
              onClick={closeMenu}
            >
              Login
            </Link>
          ) : (
            <Link
              to="/logout"
              className="drawer-item logout-btn"
              onClick={closeMenu}
            >
              Logout
            </Link>
          )}
        </div>
      </div>

      {/* Backdrop overlay */}
      {isMenuOpen && <div className="menu-overlay" onClick={closeMenu}></div>}
    </>
  );
};

export default Navbar;