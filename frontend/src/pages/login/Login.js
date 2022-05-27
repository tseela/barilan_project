import './Login.css';
import { Navbar } from '../../components';
import { LoginDialog, Logout } from '../../components';
import { useToken } from '../../hooks';

export default function Login() {
    const { token, setToken } = useToken();

    if (token) {
        return(
            <main className='login'>
                <script>alert("You need to logout first!")</script>
                <header className='navbar'>
                    <Navbar />
                </header>
                <Logout setToken={setToken} />
            </main>
        );
    }

    return (
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

