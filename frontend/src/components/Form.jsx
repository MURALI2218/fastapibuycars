import { useState } from "react";
import api from '../api'
import {  useNavigate } from "react-router-dom";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../constant"
import '../sytles/loginform.css'

import { Link } from "react-router-dom";


function Form({route,method}){
    const [username, setUsername] = useState('')
    const [password, setPassword] =useState('')
    const [loading, setLoading] = useState(false)

    const navigate = useNavigate()
    const name = method === "login"?'Login':"Register"

    const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
        const formData = new URLSearchParams();

        formData.append("username", username);
        formData.append("password", password);

        const res = await api.post(route, formData);

        if (method === "login") {
            localStorage.setItem(
                ACCESS_TOKEN,
                res.data.access_token
            );

            navigate("/");
        } else {
            navigate("/login");
        }

    } catch (error) {

        if (error.response) {
           
            alert(error.response.data.detail);
        } else {
            alert("Unable to connect to server");
        }

    } finally {
        setLoading(false);
    }
};

    return (
    <form  onSubmit={handleSubmit} className ='user-from'>
        <h1>{name}</h1>
        <input className="form-input" type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="hello@gamil.com"
            required
        ></input>
        <input
            className="form-input"
            type="password"
            value ={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Password"
            required
        ></input>
        <div>
             <button className="form-button" type="submit">
            {name}
        </button>
         { name === "Login" && (
            <p className="register-link">
                New User? <Link to="/register">Register</Link>
            </p>
        )}

        </div>
       
     </form>
    )
}

export default Form