import './Profile.css';
import { Navbar } from '../../components';
import { useToken } from '../../hooks';

export default function Profile() {
    const { token, setToken } = useToken();

    if (!token) {
        return(
            <main className='profile'>
                <header className='navbar'>
                    <Navbar />
                </header>
                <div>You need to log in first!<br></br><a href='/signin'>Login</a></div>
            </main>
        );
    }

    return (
        <main className='profile'>
            <header className='navbar'>
                <Navbar />
            </header>
            <div>replace with user profile</div>
        </main>
    );
}

