import './EditTrip.css';
import PropTypes from 'prop-types';
import { useState } from 'react';
import { Navbar, DisplayTrip } from '../../components';

export default function OfflineEditTrip({ trip, saveEditedTrip }) {
    const [ editedTrip, setEditedTrip ] = useState(null);
    const [ editedTripName, setEditedTripName ] = useState('');

    function saveTrip() {
        if (editedTripName === '') {
            return;
        }
        et.name = editedTripName;
        let et = editedTrip;

        saveEditedTrip(et);
    }

    // else, everything is ok and we are ready to display the trip
    return(
        <div className='edittrip'>
            <Navbar />
            <div className='display'>
                <div className='edit-row'>
                    <form onSubmit={saveTrip}>
                        <label>
                                <div className='display-name'>
                                    Trip name:
                                </div>
                                <input className='form' type="text" placeholder={trip?.name} maxLength="16" onChange={e => setEditedTripName(e.target.value)} />
                        </label>
                        <div className='savetrip'><button className='savetrip-button' type={"submit"}>Save</button></div>
                    </form>
                </div>
                <div className='display-edittrip'>
                    <DisplayTrip trip={trip} canSort={true} setEditedTrip={setEditedTrip} />
                </div>
            </div>
        </div>
    )
}

OfflineEditTrip.propTypes = {
    trip: PropTypes.object.isRequired,
    saveEditedTrip: PropTypes.func.isRequired
}