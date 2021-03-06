import './Profile.css';
import { Navbar } from '../../components';
import { useToken } from '../../hooks';
import { Navigate } from 'react-router-dom';
import { useEffect, useState } from 'react';

/**
 * user profile page
 * 
 * @returns 
 */
export default function Profile() {
    const { token, setToken } = useToken(); // user token
    const [ trips, setTrips ] = useState([]); // trips array

    useEffect(() => {
        // if user connected
        if (token) {
            // get name&id of user's trips
            fetch('/getTripsAndNamesByUser', {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json'
                },
                body: JSON.stringify({'username': token.user, 'token':token})
            }).then((res) => res.json()).then((res) => {
                setTrips(res); // update trips
            });
        }
    }, [token]);

    // don't allow when user isn't connected
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
                    {token.user}
                </div>
                {/* array of trips names (onclick->link to viewtrip) */}
                <div className='profile-trips'>
                    <ul className='trips-ul'>
                        {trips.map((trip) => { return <li key={trip.id}><a href={"/viewtrip/" + trip.id}>{trip.name}</a></li> })}
                    </ul>
                </div>
            </div>
        </main>
    );
}

