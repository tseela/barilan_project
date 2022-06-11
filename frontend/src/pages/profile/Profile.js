import './Profile.css';
import { Navbar } from '../../components';
import { useToken } from '../../hooks';
import { Navigate } from 'react-router-dom';
import { useEffect, useState } from 'react';

export default function Profile() {
    const { token, setToken } = useToken();
    const [ trips, setTrips ] = useState([]);

    useEffect(() => {
        if (token) {
            fetch('/getusertrips', {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json'
                },
                body: JSON.stringify({username: token[0].user})
            }).then((res) => res.json()).then((res) => {
                setTrips(res);
            });
        } else {
            setTrips([]);
        }
    }, [token]);

    if (!token) {
        alert("You need to log in first.");
        return(
            <Navigate to='/login' />
        );
    }
    

    return (
        <main className='profile-page'>
            <header className='navbar'>
                <Navbar />
            </header>
            <div className='profile-body'>
                <div className='profile-username'>
                    {token[0]?.user}
                </div>
                <div className='profile-trips'>
                    <ul className='trips-ul'>
                        {trips.map((trip) => { return <li key={trip.id}><a href={"/trip/" + trip.id}>{trip.name}</a></li> })}
                    </ul>
                </div>
            </div>
        </main>
    );
}

