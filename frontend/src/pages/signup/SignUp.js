import './SignUp.css';
import { Navbar } from '../../components';
import { SignUpDialog, Logout } from '../../components';
import { useToken } from '../../hooks';

export default function Login() {
    const { token, setToken } = useToken();

    if (token) {
        return(
            <main className='signup'>
                <script>alert("You need to logout first!")</script>
                <header className='navbar'>
                    <Navbar />
                </header>
                <Logout setToken={setToken} />
            </main>
        );
    }

    return (
        <main className='signup'>
            <header className='navbar'>
                <Navbar />
            </header>
            <SignUpDialog setToken={setToken} />
        </main>
    );
}

