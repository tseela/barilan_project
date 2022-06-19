import './PlanTrip.css';
import { useToken } from '../../hooks';
import { OfflineEditTrip } from '../index';
import { useState, useEffect } from 'react';
import { Loading, Navbar, LoginDialog, SignUpDialog } from '../../components';
import { Navigate } from 'react-router-dom';

export default function PlanTrip() {
    const { token, setToken } = useToken();
    const [ trip, setTrip ] = useState(null);
    const [ isLoading, setIsLoading ] = useState(false);
    const [ checkBoxes, setCheckBoxValues ] = useState({ 'a':true, 'b':false });
    const [ isDone, setIsDone ] = useState(false);
    const [ shouldLogin, setShouldLogin ] = useState(true);

    const handleSubmit = async e => {
        e.preventDefault();
        // check validity
        // setIsLoading(true) -> fetch request for new trip -> setIsLoading(false)
    }

    function saveTrip(tripToSave) {
        if (!token) {
            alert("You need to login first!");
            setShouldLogin(true);
        } else {
            fetch('/insertTripToUser', {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json'
                },
                body: JSON.stringify({'token':token, 'trip':tripToSave})
            }).then((res) => {
                if (res.status === 200) {
                    alert("Success! Trip saved.");
                    setIsDone(true);
                } else {
                    alert("Something went wrong... Your trip couldn't be saved.");
                }
            });
        }
    }

    if (isDone) {
        return(<Navigate to='/home' />);
    }

    if (isLoading) { // loading screen
        return(
            <div className='plantrip-container'>
                <Navbar />
                <div className='loading-div'>
                    <Loading />
                </div>
            </div>
        );
    }

    if (!token && shouldLogin) {
        return(
            <div className='plantrip-container'>
                <Navbar />
                <div className='delayed-login-div'>
                    <div className='delayed-login dialog'><LoginDialog setToken={setToken} directToRegister={false} /></div>
                    <div className='delayed-signup dialog'><SignUpDialog alertSignUp={() => {}} directToLogin={false} /></div>
                </div>
            </div>
        );
    }

    if (!trip) {
        return(
            <div className='re-render'>
                <div className='plantrip-container'>
                    <Navbar />
                </div>
            </div>
        );
    }

    if (trip) { // trip is set -> display it
        return(<OfflineEditTrip trip={trip} saveEditedTrip={saveTrip} />);
    }
}