import './EditTrip.css';
import PropTypes from 'prop-types';
import { useState } from 'react';
import { Navbar, DisplayTrip } from '../../components';
import cloneDeep from 'lodash/cloneDeep';

/**
 * offline page where you edit a given trip
 * 
 * @param trip
 * @param saveEditedTrip - func to save the trip after editing
 * @returns 
 */
export default function OfflineEditTrip({ trip, saveEditedTrip, canCancel=true, alertCancel }) {
    const [ editedTrip, setEditedTrip ] = useState(cloneDeep(trip)); // edited trip
    const [ editedTripName, setEditedTripName ] = useState(''); // edited trip name

    // changes trip name if needed and saving it
    function saveTrip(e) {
        e.preventDefault();
        
        if (editedTripName === '') {
            alert('You must name your trip!');
            return;
        }
        let et = cloneDeep(editedTrip);
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
                        {/* edited name and savetrip button */}
                        <label className='edit-name'>Trip name:</label>
                        <input className='edited-name' type="text" maxLength="16" onChange={(e) => setEditedTripName(e.target.value)} />
                        {canCancel ? <button className='cancel-button' onClick={() => alertCancel()}>Cancel Changes</button> : ''}
                        <label className='savetrip'>
                            <button className='savetrip-button' type={"submit"}>Save</button>
                        </label>
                    </form>
                </div>
                {/* trip display with option to sort activities */}
                <div className='display-edittrip'>
                    <DisplayTrip trip={trip} canSort={true} setEditedTrip={setEditedTrip} />
                </div>
            </div>
        </div>
    )
}

OfflineEditTrip.propTypes = {
    trip: PropTypes.object.isRequired,
    saveEditedTrip: PropTypes.func.isRequired,
    canCancel: PropTypes.bool,
    alertCancel: PropTypes.func
}