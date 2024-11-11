import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import LoginForm from './LoginForm';
import SignUp from './SignUpForm';
import './Login.css';
import './App.css';
import logo from './assets/download (2).png';

const Header = () => {
    return (
        <header className="header">
            <div className="logo-container">
                <img src="https://placeholder.pics/svg/50x50" alt="Logo" className="logo" />
                <span className="app-name">MEDICINE DELIVERY APP</span>
            </div>
            <nav className="nav-links">
                <a href="#about">About</a>
                <a href="#shop">Shop</a>
                <a href="#cart">Shopping Cart</a>
                <a href="#doctors">Doctors</a>
            </nav>
            <div className="auth-buttons">
                <button className="login-button"><Link to="/login">LOGIN</Link></button>
                <button className="signup-button"><Link to="/signup">SIGN UP</Link></button>
            </div>
        </header>
    );
};

const HeroSection = () => (
    <div className="hero-container">
        <div className="hero-content">
            <h1>Your Health, Delivered to Your Doorstep!</h1>
            <p>
                Get medicines, health essentials, and more — anytime, anywhere! Fast delivery,
                trusted brands, and exclusive discounts. Order now and experience hassle-free,
                reliable healthcare from the comfort of your home!
            </p>
        </div>
        <div className="hero-image">
            <img src={logo} alt="Delivery Illustration" />
        </div>
    </div>
);

const AboutSection = () => {
    return (
        <div className="about-container">
            <h1 className="about-header">About Us</h1>
            <p>
                Welcome to MEDICURE, your trusted partner in health and wellness. Our mission is to make
                quality healthcare accessible, convenient, and reliable for everyone. We understand that
                your health is your most valuable asset, which is why we’re dedicated to providing you with
                a wide range of essential medical products, from prescription medications to daily health
                essentials, all in one place.
                At MEDICURE, we take pride in offering a seamless online experience, ensuring that you can
                easily find and purchase the products you need with just a few clicks. We work with licensed
                pharmacies, certified suppliers, and healthcare professionals to guarantee that every product
                meets the highest standards of quality and safety. Our platform is designed to provide you with
                quick, reliable deliveries, secure transactions, and the peace of mind that comes from knowing
                you’re getting genuine products.
                With a team of experienced professionals and a customer-first approach, we are committed to
                supporting your health journey. Whether you need expert advice, have questions about a medication,
                or simply need help with your order, our support team is here to assist you every step of the way.
                Your health, convenience, and satisfaction are our top priorities. Thank you for choosing MEDICURE
                as your health and wellness partner.
            </p>
        </div>
    );
};


function App() {
  return (
    <Router>
      <div >
        <Header />
        <HeroSection />
        <AboutSection />
        <nav>
          <ul>
            <li>
              <Link to="/login">Login</Link>
            </li>
            <li>
              <Link to="/signup">Sign Up</Link>
            </li>
          </ul>
        </nav>

        <Routes>
          <Route path="/login" element={<LoginForm />} />
          <Route path="/signup" element={<SignUp />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
