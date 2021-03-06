import './EditTrip.css';
import { useToken } from '../../hooks';
import { Forbidden } from '../index';
import { useState, useEffect } from 'react';
import { Loading, Navbar, DisplayTrip } from '../../components';
import { Navigate } from 'react-router-dom';
import cloneDeep from 'lodash/cloneDeep';

/**
 * page where you edit trip with given id
 * url looks like that: https//:host/edittrip/id
 * 
 * @returns 
 */
export default function EditTrip() {
    const { token, setToken } = useToken(); // user token
    const [ trip, setTrip ] = useState(null); // trip to edit
    const [ editedTrip, setEditedTrip ] = useState(null); // the trip after editings
    const [ editedTripName, setEditedTripName ] = useState(''); // edited trip name
    const [ status, setStatus ] = useState(true); // true->all good, false->forbidden access
    const [ isLoading, setIsLoading ] = useState(false); // should show loader
    const [ isDone, setIsDone ] = useState(false); // after finishing

    // extruct id from url
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
                    if (res[i]?.id === id) {
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
                    setTimeout(() => {
                        setTrip(res);
                        setTimeout(() => setEditedTrip(cloneDeep(trip)), 500);
                    }, 500); //wait 1 sec
                }
            }));
        }
    }, [token]);

    // updates trip in db
    function updateTrip(edited) {
        fetch('/updateTrip', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({'token':token, 'trip':edited})
        }).then((res) => {
            if (res.status === 200) {
                alert("Success! Trip saved.");
                setIsDone(true);
            } else {
                alert("Something went wrong... Your trip couldn't be saved.");
            }
            setIsLoading(false);
        });
    }

    // save trip after editing
    const saveEditedTrip = async (e) => {
        e.preventDefault();

        if (!editedTrip) {
            alert("Error in saving changes. Please try again in a few seconds.");
            setEditedTrip(cloneDeep(trip));
            return;
        }

        setIsLoading(true);
        let et = cloneDeep(editedTrip);
        setTimeout(() => {
            // update edited name
            if (editedTripName !== '' && editedTripName !== trip?.name) {
                et.name = editedTripName;
            }
            updateTrip(et);
        }, 1000);
    }

    // trip is already saved-> return to viewtrip of it
    if (isDone) {
        return(<Navigate to={"/viewtrip/" + id} />);
    }

    // can't edittrip if you are not connected
    // can't also if the requested trip is not yours
    if (!token || !status) {
        return(<Forbidden />);
    }

    // if status if ok and trip in still null, show that we are loading the trip
    if (!trip || isLoading) {
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
                        {/* edited name, cancel button and save button */}
                        <label className='edit-name'>Trip name:</label>
                        <input className='edited-name' type="text" placeholder={trip?.name} maxLength="16" onChange={(e) => setEditedTripName(e.target.value)} />
                        <button className='cancel-button' onClick={() => setIsDone(true)}>Cancel Changes</button>
                        <label className='savetrip'>
                            <button className='savetrip-button' type={"submit"}>Save</button>
                        </label>
                    </form>
                </div>
                {/* trip display (with ability to sort) */}
                <div className='display-edittrip'>
                    <DisplayTrip trip={trip} canSort={true} setEditedTrip={setEditedTrip} />
                </div>
            </div>
        </div>
    )
}