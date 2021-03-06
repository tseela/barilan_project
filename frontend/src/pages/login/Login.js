import './Login.css';
import { Navbar } from '../../components';
import { LoginDialog } from '../../components';
import { useToken } from '../../hooks';
import { Navigate } from "react-router-dom";

/**
 * login page
 * 
 * @returns 
 */
export default function Login() {
    const { token, setToken } = useToken(); // user token

    // don't allow if user is already connected
    if (token) {
        return(<Navigate to="/home" />);
    }

    return(
        <main className='login'>
            <header className='navbar'>
                <Navbar />
            </header>
            <div className='login-dialog'>
                <LoginDialog setToken={setToken} />
            </div>
        </main>
    );
}

