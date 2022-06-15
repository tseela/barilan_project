import './DisplayTrip.css';
import PropTypes from 'prop-types';
import DisplayDay from '../displayday/DisplayDay';
import { useState } from 'react';

// {JSON.stringify(trip.days[0].activities[0])}
export default function DisplayTrip({ trip, setEditedTrip }) {
    const [ displayed, setDisplayed ] = useState({ title:'', link:'' });

    // src="https://maps.google.com/maps?q=COORDINATES&t=&z=13&ie=UTF8&iwloc=&output=embed"
    return(
    <div className="displaytrip-container">
        <div className='activities-display'>
            {trip?.days.map((d, i) => { return <DisplayDay day={d} index={i} key={i} setEditedTrip={setEditedTrip} notifyPressed={(_title, _link) => setDisplayed({ title:_title, link:_link })} /> })}
        </div>
        <div className='displayitem'>
            <iframe className='googlemaps' title='info' src={displayed.link[0]}></iframe>
        </div>
    </div>
    )
}

DisplayTrip.propTypes = {
    trip: PropTypes.object.isRequired,
    setEditedTrip: PropTypes.func
}