import Form from '../components/Form'
import Navbar from './Navbar'
function Login(){
    
    return <>
        <Navbar></Navbar>
        <Form route='/api/login/' method='login' ></Form>
    </>
}

export default Login