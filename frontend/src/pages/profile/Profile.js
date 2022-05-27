import './Profile.css';
import { Navbar } from '../../components';
import { useToken } from '../../hooks';

export default function Profile() {
    const { token, setToken } = useToken();

    if (!token) { //alert("You need to log in first!") and move straight to /signin
        return(
            <main className='profile'>
                <header className='navbar'>
                    <Navbar />
                </header>
                <div className='body'>You need to log in first!<br></br><a href='/login'>Login</a></div>
            </main>
        );
    }

    return (
        <main className='profile'>
            <header className='navbar'>
                <Navbar />
            </header>
            <div className='body'>replace with user profile</div>
        </main>
    );
}

