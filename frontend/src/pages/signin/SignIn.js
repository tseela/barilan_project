import './SignIn.css';
import { Navbar } from '../../components';
import { Login, Logout, SignUp } from '../../components';
import { useToken } from '../../hooks';
import { useState } from 'react';

export default function SignIn() {
    const { token, setToken } = useToken();
    const [ hasUser, setHasUser ] = useState(true);

    function ChangeHasUser() {
        setHasUser(!hasUser);
    }

    if (token) {
        return(
            <main className='signin'>
                <header className='navbar'>
                    <Navbar />
                </header>
                <Logout setToken={setToken} />
            </main>
        );
    }

    return (
        <main className='signin'>
            <header className='navbar'>
                <Navbar />
            </header>
            { hasUser ? <div>
                <Login setToken={setToken} />
                <div>You don't have a user?<br></br>
                    <button onClick={ChangeHasUser}>Sign Up</button>
                </div>
            </div> : null }
            { !hasUser ? <div>
                <SignUp setToken={setToken} />
                <div>You allready have a user?<br></br>
                    <button onClick={ChangeHasUser}>Login</button>
                </div>
            </div> : null }
        </main>
    );
}

