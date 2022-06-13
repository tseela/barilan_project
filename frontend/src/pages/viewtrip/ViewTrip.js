import './ViewTrip.css';
import { useToken } from '../../hooks';
import { Forbidden } from '../index';
import { useState, useEffect } from 'react';
import { Loading, Navbar } from '../../components';

export default function ViewTrip() {
    const { token, setToken } = useToken();
    const [ trip, setTrip ] = useState(null);
    const [ status, setStatus ] = useState(true); // true->all good, false->forbidden access
    const id = window.location.pathname;

    useEffect(() => {
        // if the user is connected
        if (token) {
            // ask for the trip
            fetch('/getTrip', {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json'
                },
                body: JSON.stringify({tripID: id, token:token})
            }).then((res) => {
                if (res.status === 200) {
                    return res.json();
                }
                return null;
            }).then((res) => {
                if (!res) { // if response status is not ok update
                    setStatus(false);
                } else { // status ok, update trip in 1 sec
                let delay_res = res;
                    setTimeout((delay_res) => {
                        setTrip(res);
                    }, 1000); //wait 1 sec
                }
            });
        }
    }, [token]);

    // can't viewTrip if you are not connected
    // can't also if the requested trip is not yours
    if (!token || !status) {
        return(<Forbidden />);
    }

    // if status if ok and trip in still null, show that we are loading the trip
    if (!trip) {
        return(
            <div className='loading-container'>
                <Navbar />
                <div className='loading-div'>
                    <Loading />
                </div>
            </div>
        );
    }

    // else, everything is ok and we are ready to display the trip
    return(
        <div className='viewtrip'>
            {JSON.stringify(trip, undefined, 1)}
        </div>
    )
}