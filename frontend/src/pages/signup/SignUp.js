import './SignUp.css';
import { Navbar } from '../../components';
import { SignUpDialog } from '../../components';
import { useToken } from '../../hooks';
import { Navigate } from 'react-router-dom';
import { useState } from 'react';

export default function Login() {
    const { token, setToken } = useToken();
    const [ isSigned, setIsSigned ] = useState(false);

    // don't allow if user is allready connected
    if (token) {
        return(<Navigate to="/home" />);
    }

    // address users who just signed up to login page
    if (isSigned) {
        return(<Navigate to="/login" />);
    }

    return (
        <main className='signup'>
            <header className='navbar'>
                <Navbar />
            </header>
            <div className='signup-dialog'>
                <SignUpDialog alertSignUp={() => setIsSigned(true) } />
            </div>
        </main>
    );
}

