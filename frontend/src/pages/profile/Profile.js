import './Profile.css';
import { Navbar } from '../../components';
import { useToken } from '../../hooks';
import { Navigate } from 'react-router-dom';

export default function Profile() {
    const { token, setToken } = useToken();

    if (!token) {
        alert("You need to log in first.");
        return(
            <Navigate to='/login' />
        );
    }

    let username = token[0]?.user;
    
    let trips = [];
    for (let i = 1; i < 9; ++i) {
        trips.push({id:i, name:"trip" + i});
    }

    const listItems = trips.map((trip) => <li><a href={"/trip/" + trip.id}>{trip.name}</a></li>);


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

