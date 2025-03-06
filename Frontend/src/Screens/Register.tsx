import { ChangeEventHandler, FormEventHandler, useState } from "react";
import { useNavigate } from "react-router";
import apiFetcher from "@/lib/apiFetcher";


const Register = () => {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [passwordMatch, setPasswordMatch] = useState(true);
    const navigate = useNavigate();

  
    const handleUsernameChange : ChangeEventHandler<HTMLInputElement> = (e) => {
      setUsername(e.target.value);
    };

    const handleEmailChange : ChangeEventHandler<HTMLInputElement> = (e) => {
      setEmail(e.target.value);
    };

  
    const handlePasswordChange : ChangeEventHandler<HTMLInputElement> = (e) => {
      setPassword(e.target.value);
      setPasswordMatch(e.target.value === confirmPassword);
    };
  
    const handleConfirmPasswordChange : ChangeEventHandler<HTMLInputElement> = (e) => {
      setConfirmPassword(e.target.value);
      setPasswordMatch(e.target.value === password);
    };
  
    const handleSubmit : FormEventHandler<HTMLFormElement> = async(e) => {
      e.preventDefault();
      if (passwordMatch) {  
        await apiFetcher.register(username, email, password).then(_ => {
          navigate('/home', { state: { email } });   
        }).catch(_ => _);
      }
    };
  
    return (
      <div className="login-container w-full">
        <div className="login-box">
          <h2>Register</h2>
          <form onSubmit={handleSubmit}>
            <div className="input-group">
              <label htmlFor="username">Enter Username</label>
              <input
                type="text"
                id="username"
                placeholder="Enter your name"
                value={username}
                onChange={handleUsernameChange}
                style={{ borderColor: '#ddd' }}
                required
              />
            </div>
            <div className="input-group">
              <label htmlFor="email">Enter Email</label>
              <input
                type="email"
                id="email"
                placeholder="Enter your email"
                value={email}
                onChange={handleEmailChange}
                style={{ borderColor: '#ddd' }}
                required
              />
            </div>
            <div className="input-group">
              <label htmlFor="password">Enter Password</label>
              <input
                type="password"
                id="password"
                placeholder="Enter your password"
                value={password}
                onChange={handlePasswordChange}
                style={{ borderColor: passwordMatch ? '#ddd' : 'red' }}
                required
              />
            </div>
            <div className="input-group">
              <label htmlFor="confirmPassword">Confirm Password</label>
              <input
                type="password"
                id="confirmPassword"
                placeholder="Re-enter your password"
                value={confirmPassword}
                onChange={handleConfirmPasswordChange}
                style={{ borderColor: passwordMatch ? '#ddd' : 'red' }}
                required
              />
              {!passwordMatch && <p style={{ color: 'red' }}>Passwords do not match</p>}
            </div>
            <button type="submit" className="login-button">
              Register
            </button>
          </form>
        </div>
      </div>
    );  
}

export default Register;