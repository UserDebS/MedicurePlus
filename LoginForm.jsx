import React from "react";
import "./Login.css";

const LoginForm = () => {
  return (
    <div className="form-container">
      <div className="form-header login-header">LOGIN</div>
      <form>
        <div className="form-group">
          <label>Username</label>
          <input type="text" placeholder="Enter your username" />
        </div>
        <div className="form-group">
          <label>Password</label>
          <input type="password" placeholder="Enter your password" />
        </div>
        <button className="enter-button">ENTER</button>
      </form>
      <p className="footer-text">
        Dont have an account yet? <span>Signup!!</span>
      </p>
    </div>
  );
};

export default LoginForm;
