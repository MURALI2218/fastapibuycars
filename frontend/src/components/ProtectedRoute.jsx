import {Navigate} from "react-router-dom"
import api from '../api'
import {jwtDecode} from 'jwt-decode'
import { REFRESH_TOKEN, ACCESS_TOKEN } from "../constant"
import { useState, useEffect } from "react"

function ProtectedRoute({children}) {
    const [isAuthorized, setAuthorized] = useState(null)
    useEffect( () => {
        auth().catch(()=> setAuthorized(false)
    ) },[])

    const refreshtoken = async () => {
        const refreshtoken = localStorage.getItem(REFRESH_TOKEN)
        try{
            const res = await api.post("/api/token/refresh/", {
                refresh : refreshtoken
            });
            if (res.status === 200){
                localStorage.setItem(ACCESS_TOKEN, res.data.access)
                setAuthorized(true)
            }else{
                setAuthorized(false)
            };

        }catch(error){
            
            setAuthorized(false);
        };
    };

    const auth = async() => {
        const token = localStorage.getItem(ACCESS_TOKEN);
        
        if (!token){
            setAuthorized(false)
            return
        }
        const decoded = jwtDecode(token)
        const tokenexpiration  = decoded.exp
        const now = Date.now() / 1000

        if(tokenexpiration < now){
            await refreshtoken()
        }else{
            setAuthorized(true)
        }
    }
    if (isAuthorized === null){
        return <div>Loading...</div>

    }
 
    return isAuthorized ? children : <Navigate to="/login"/>
}
export default ProtectedRoute