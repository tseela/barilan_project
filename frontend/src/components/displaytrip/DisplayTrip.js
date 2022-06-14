import './DisplayTrip.css';
import PropTypes from 'prop-types';
import DisplayActivity from '../displayactivity/DisplayActivity';

// {JSON.stringify(trip.days[0].activities[0])}
export default function DisplayTrip({ trip, setTrip }) {
    return(
    <div className="displaytrip-container">
        <div className='activities-display'>
            <div className='day'>Day 0</div>
            {trip.days[0].activities.map((act) => { return <DisplayActivity activity={act} isRequired={null} /> })}
        </div>
    </div>
    )
}

DisplayTrip.propTypes = {
    trip: PropTypes.object.isRequired,
    setTrip: PropTypes.func.isRequired
}