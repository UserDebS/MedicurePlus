import React from "react";
import "./Login.css";

const SignUpForm = () => {
  return (
    <div className="form-container">
      <div className="form-header signup-header">Sign Up</div>
      <form>
        <div className="form-group">
          <label>Name</label>
          <input type="text" placeholder="Enter your Name" />
        </div>
        <div className="form-group">
          <label>Email</label>
          <input type="email" placeholder="Enter your Email Id" />
        </div>
        <div className="form-group">
          <label>Username</label>
          <input type="text" placeholder="Enter your Username" />
        </div>
        <div className="form-group">
          <label>Password</label>
          <input type="password" placeholder="Enter your Password" />
        </div>
        <button className="enter-button">ENTER</button>
      </form>
      <p className="footer-text">
        Already have an account? <span>Login!!</span>
      </p>
    </div>
  );
};

export default SignUpForm;
