import './ViewTrip.css';
import { useToken } from '../../hooks';
import { Forbidden } from '../index';
import { useState, useEffect } from 'react';
import { Loading, Navbar, DisplayTrip } from '../../components';
import { Navigate } from 'react-router-dom';

/**
 * page where you view trip with given id
 * url looks like that: https//:host/viewtrip/id
 * 
 * @returns 
 */
export default function ViewTrip() {
    const { token, setToken } = useToken(); // user token
    const [ trip, setTrip ] = useState(null); // trip to view
    const [ status, setStatus ] = useState(true); // true->all good, false->forbidden access
    const [ wasDeleted, setWasDeleted ] = useState(false); // did user delete trip

    // get id from url
    const id = window.location.pathname.split("/").pop();

    // get the trip from backend server
    useEffect(() => {
        // if the user is connected
        if (token) {
            // make sure the trip belongs to the user
            // get name&id of user's trips
            fetch('/getTripsAndNamesByUser', {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json'
                },
                body: JSON.stringify({'username': token.user, 'token':token})
            }).then((res) => res.json()).then((res) => {
                for (let i = 0; i < res.length; ++i) {
                    if (res[i]?.id == id) {
                        return;
                    }
                }
                setStatus(false);
            }).then(fetch('/getTrip', {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json'
                },
                body: JSON.stringify({'tripID': id, 'token':token})
            }).then((res) => {
                if (res.status === 200) {
                    return res.json();
                }
                return null;
            }).then((res) => {
                if (!res || !status) { // if response status is not ok update
                    setStatus(false);
                } else { // status ok, update trip
                    setTimeout(() => {
                        setTrip(res);
                        console.log(res);
                    }, 500);
                }
            }));
        }
    }, [token]);

    // deletes a trip
    function deleteTrip() {
        fetch('/removeTripFromUser', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({'id': id, 'token':token, 'user':token?.user})
        }).then((res) => {
            if (res.status === 200) {
                alert("Trip deleted successfully");
                setWasDeleted(true);
            } else {
                alert("ERROR: Couldn't delete trip.")
            }
        });
    }

    // if trip is deleted, get back to profile
    if (wasDeleted) {
        return(<Navigate to="/profile" />)
    }

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
            <Navbar />
            <div className='display'>
                <div className='display-row'>
                    {/* name, edittrip button and deletetrip button */}
                    <div className='display-name'>Trip name: <span>{trip?.name}</span></div>
                    <div className='edittrip-div'>
                        <a className='edittrip-button' href={'/edittrip/' + id}>Edit Trip</a>
                        <button className='deletetrip-button' onClick={deleteTrip}>Delete Trip</button>
                    </div>
                </div>
                <div className='displaytrip'>
                    <DisplayTrip trip={trip} />
                </div>
            </div>
        </div>
    )
}