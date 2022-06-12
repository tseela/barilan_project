import './SignUp.css';
import { Navbar } from '../../components';
import { SignUpDialog } from '../../components';
import { useToken } from '../../hooks';
import { Navigate } from 'react-router-dom';

export default function Login() {
    const { token, setToken } = useToken();

    if (token) {
        return(<Navigate to="/home" />);
    }

    return (
        <main className='signup'>
            <header className='navbar'>
                <Navbar />
            </header>
            <div className='signup-dialog'>
                <SignUpDialog setToken={setToken} />
            </div>
        </main>
    );
}

