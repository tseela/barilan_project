import './SignUp.css';
import { Navbar } from '../../components';
import { SignUpDialog } from '../../components';
import { useToken } from '../../hooks';
import { Navigate } from 'react-router-dom';
import { useState } from 'react';

/**
 * signup page
 * 
 * @returns 
 */
export default function SignUp() {
    const { token, setToken } = useToken(); // user token
    const [ isSigned, setIsSigned ] = useState(false); // is done

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

