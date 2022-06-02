import './Profile.css';
import { Navbar } from '../../components';
import { useToken } from '../../hooks';

export default function Profile() {
    const { token, setToken } = useToken();
    let username = token[0]?.user;
    const trips = [{id:1, name:"trip1"}, {id:2, name:"trip2"}, {id:3, name:"trip3"}];
    const listItems = trips.map((trip) => <li key={trip.id}>{trip.name}</li>);

    if (!token) {
        return(
            <main className='profile-page'>
                <header className='navbar'>
                    <Navbar />
                </header>
                <div className='connect body'>You need to log in first!<br></br><a href='/login'>Login</a></div>
            </main>
        );
    }

    return (
        <main className='profile-page'>
            <header className='navbar'>
                <Navbar />
            </header>
            <div className='profile body'>
                <div className='profile-username'>
                    {username}
                </div>
                <div className='profile-trips'>
                    <ul>{listItems}</ul>
                </div>
            </div>
        </main>
    );
}

