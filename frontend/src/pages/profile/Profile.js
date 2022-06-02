import './Profile.css';
import { Navbar } from '../../components';
import { useToken } from '../../hooks';

export default function Profile() {
    const { token, setToken } = useToken();
    let username = token[0]?.user;
    
    let trips = [];
    for (let i = 1; i < 10; ++i) {
        trips.push({id:i, name:"trip" + i});
    }

    const listItems = trips.map((trip) => <li><a href={"/trip/" + trip.id}>{trip.name}</a></li>);

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
                    <ul className='trips-ul'>{listItems}</ul>
                </div>
            </div>
        </main>
    );
}

