import './DisplayTrip.css';
import PropTypes from 'prop-types';
import DisplayDay from '../displayday/DisplayDay';
import DisplayActivity from '../displayactivity/DisplayActivity';

// {JSON.stringify(trip.days[0].activities[0])}
export default function DisplayTrip({ trip, setTrip }) {
    return(
    <div className="displaytrip-container">
        <div className='activities-display'>
            {trip?.days.map((d, i) => { return <DisplayDay day={d} index={i} key={i} /> })}
        </div>
    </div>
    )
}

DisplayTrip.propTypes = {
    trip: PropTypes.object.isRequired,
    setTrip: PropTypes.func
}