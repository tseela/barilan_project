import './Profile.css';
import { Navbar } from '../../components';
import { Login } from '../../pages';
import { useToken } from '../../hooks';

export default function Profile() {
    const { token, setToken } = useToken();

    if(!token) {
      return <Login token={token} setToken={setToken} />
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

