import Login from './pages/login'
import Register from './pages/register'
import Home from './pages/home'
import Notfound404 from './pages/Notfound'
import Owncarslist from "./pages/owncars"
import ProtectedRoute from "./components/ProtectedRoute"
import { BrowserRouter, Navigate, Route , Routes} from "react-router-dom"
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import Profile from './pages/profile'
import { ACCESS_TOKEN } from './constant';
import { jwtDecode } from "jwt-decode";
import Bookings from './pages/booking'
const token = localStorage.getItem(ACCESS_TOKEN);
if (token === String){
  const decoded = jwtDecode(token);

console.log(decoded);
}


function Logout() {
  localStorage.clear()
  return <Navigate to='/login' />
}
function RegisterandLogout(){
  localStorage.clear()
  return <Register ></Register>
}

function App() {
  return (
    <>
      <BrowserRouter>
        <Routes>
        <Route path='/' element={ <Home/>} />
        <Route path='/login' element = {<Login></Login>}></Route>
        <Route path='/register' element= { <RegisterandLogout></RegisterandLogout>}></Route>
        <Route path='/logout' element={<Logout></Logout>}> </Route>
        <Route path="*" element={<Notfound404></Notfound404>}></Route>
        <Route path='/owncarslist' element={<ProtectedRoute><Owncarslist/></ProtectedRoute>}></Route>
        <Route path="/profile"element={ <ProtectedRoute><Profile /> </ProtectedRoute>}/>
        <Route path="/carbooking" element={ <ProtectedRoute><Bookings /></ProtectedRoute>}/>
       </Routes>
      </BrowserRouter>

      <ToastContainer position="top-right" autoClose={3000}/>
    </>
  )
}

export default App
