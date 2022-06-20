import './EditTrip.css';
import { useToken } from '../../hooks';
import { Forbidden } from '../index';
import { useState, useEffect } from 'react';
import { Loading, Navbar, DisplayTrip } from '../../components';
import { Navigate } from 'react-router-dom';

export default function EditTrip() {
    const { token, setToken } = useToken();
    const [ trip, setTrip ] = useState(null);
    const [ editedTrip, setEditedTrip ] = useState(null);
    const [ status, setStatus ] = useState(true); // true->all good, false->forbidden access
    const [ editedTripName, setEditedTripName ] = useState('');
    const [ isDone, setIsDone ] = useState(false);

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
                } else { // status ok, update trip in 1 sec
                let delay_res = res;
                    setTimeout((delay_res) => {
                        setTrip(res);
                    }, 1000); //wait 1 sec
                }
            }));
        }
    }, [token]);

    const saveEditedTrip = async (e) => {
        e.preventDefault();

        let et = editedTrip;
        if (editedTripName !== '' && editedTripName !== trip?.name) {
            et.name = editedTripName;
        }

        fetch('/insertTripToUser', { // should by updateTrip
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({'token':token, 'trip':et})
        }).then((res) => {
            if (res.status === 200) {
                alert("Success! Trip saved.");
                setIsDone(true);
            } else {
                alert("Something went wrong... Your trip couldn't be saved.");
            }
        });
    }

    // trip is already saved-> return to viewtrip of it
    if (isDone) {
        return(<Navigate to={"/viewtrip/" + id} />)
    }

    // can't edittrip if you are not connected
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
        <div className='edittrip'>
            <Navbar />
            <div className='display'>
                <div className='edit-row'>
                    <form onSubmit={saveEditedTrip} className="form-horizontal">
                        <label className='edit-name'>Trip name:</label>
                        <input className='edited-name' type="text" placeholder={trip?.name} maxLength="16" onChange={(e) => setEditedTripName(e.target.value)} />
                        <button className='cancel-button' onClick={() => setIsDone(true)}>Cancel Changes</button>
                        <label className='savetrip'>
                            <button className='savetrip-button' type={"submit"}>Save</button>
                        </label>
                    </form>
                </div>
                <div className='display-edittrip'>
                    <DisplayTrip trip={trip} canSort={true} setEditedTrip={setEditedTrip} />
                </div>
            </div>
        </div>
    )
}