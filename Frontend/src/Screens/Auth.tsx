import apiFetcher from "@/lib/apiFetcher";
import { ChangeEvent, FormEventHandler, useEffect, useState } from "react";
import { useNavigate } from "react-router";

const Auth = () => {
    const navigator = useNavigate()
    useEffect(() => {
        (async() =>{apiFetcher.authByToken().then(res => {
            if(res.status == 200) navigator('/home')
        }).catch(_ => _);})()
    }, [])
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const handleEmailChange = (e : ChangeEvent<HTMLInputElement>) => {
        setEmail(e.target.value);
    };

    const handlePasswordChange = (e : ChangeEvent<HTMLInputElement>) => {
        setPassword(e.target.value);
    };

    const handleSubmit : FormEventHandler<HTMLFormElement> = async(e) => {
        e.preventDefault();
        await apiFetcher.authByUserPass(email, password).then(res => {
            if(res.status === 200) navigator('/home');
        }).catch(_ => console.log(_))
        console.log('Login Details:', { email, password });
    };

    return (
        <div className="login-container">
            <div className="login-box">
                <h2>Login</h2>
                <form onSubmit={handleSubmit}>
                    <div className="input-group">
                        <label htmlFor="email">Email</label>
                        <input
                            type="text"
                            id="email"
                            placeholder="Enter your email"
                            value={email}
                            onChange={handleEmailChange}
                            required
                        />
                    </div>
                    <div className="input-group">
                        <label htmlFor="password">Password</label>
                        <input
                            type="password"
                            id="password"
                            placeholder="Enter your password"
                            value={password}
                            onChange={handlePasswordChange}
                            required
                        />
                    </div>
                    <button type="submit" className="login-button">
                        Login
                    </button>
                </form>
                <p className="register-link">
                    Don't have an account? <a href="/signup">Register here</a>
                </p>
            </div>
        </div>
    );
}



export default Auth;