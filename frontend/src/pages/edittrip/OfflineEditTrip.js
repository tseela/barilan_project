import './EditTrip.css';
import PropTypes from 'prop-types';
import { useState } from 'react';
import { Navbar, DisplayTrip } from '../../components';
import cloneDeep from 'lodash/cloneDeep';

export default function OfflineEditTrip({ trip, saveEditedTrip }) {
    const [ editedTrip, setEditedTrip ] = useState(cloneDeep(trip));
    const [ editedTripName, setEditedTripName ] = useState('');

    function saveTrip() {
        if (editedTripName === '') {
            return;
        }
        let et = editedTrip;
        et.name = editedTripName;

        saveEditedTrip(et);
    }

    // else, everything is ok and we are ready to display the trip
    return(
        <div className='edittrip'>
            <Navbar />
            <div className='display'>
                <div className='edit-row'>
                    <form onSubmit={saveTrip} className="form-horizontal">
                        <label className='edit-name'>Trip name:</label>
                        <input className='edited-name' type="text" maxLength="16" onChange={(e) => setEditedTripName(e.target.value)} />
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

OfflineEditTrip.propTypes = {
    trip: PropTypes.object.isRequired,
    saveEditedTrip: PropTypes.func.isRequired
}