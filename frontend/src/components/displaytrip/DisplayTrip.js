import './DisplayTrip.css';
import PropTypes from 'prop-types';
import DisplayDay from './displayday/DisplayDay';
import GoogleMapsMap from '../maps/googlemaps/GoogleMapsMap';
import Flights from './flights/Flights';
import { useRef, useState } from 'react';
import cloneDeep from 'lodash/cloneDeep';

export default function DisplayTrip({ trip, canSort, setEditedTrip }) {
    const [ displayed, setDisplayed ] = useState({ 'title':'', 'latitude':'', 'longitude':'' });
    const [ picArray, setPicArray ] = useState([]);
    const [ picIndex, setPicIndex ] = useState(-1);

    // after load, update editedTrip to be trip
    useRef(() => {
        if (canSort && typeof setEditedTrip !== 'undefined') {
            setEditedTrip(cloneDeep(trip));
        }
    }, []);

    // report on trip change
    function report(sortedInts, dayIndex) { // using cloneDeep to copy nested arrays and jsons
        let reorderedActivities = sortedInts.map((i) => { return cloneDeep(trip?.days[dayIndex]?.activities[i]); })
        let newTrip = cloneDeep(trip);
        newTrip.days[dayIndex] = {
            activities: cloneDeep(reorderedActivities)
        }
        setEditedTrip(newTrip);
    }

    // move to previous pic if u can
    function clickLeft() {
        if (picIndex > 0) {
            setPicIndex(picIndex - 1);
        }
    }

    // move to next pic if u can
    function clickRight() {
        if (picIndex < picArray.length - 1) {
            setPicIndex(picIndex + 1);
        }
    }

    // can use openstreetmap instead of google maps but they don't have a marker...
    return(
    <div className="displaytrip-container">
        <div className='reg-page-container' style={{opacity: picIndex === -1 ? 1 : 0.5}}>
            <div className='activities-display'>
                <Flights transports={trip?.initFlight} notifyPressed={() => {}} />
                {trip?.days.map((d, i) => { return <DisplayDay reportSorting={(sortedInts) => report(sortedInts, i)} day={d} index={i} key={i} canSort={canSort} iconPressed={(img_array) => {if (img_array.length !== 0) { setPicArray(img_array); setPicIndex(0);}}} setEditedTrip={setEditedTrip} notifyPressed={(_title, _coordinates) => setDisplayed({ 'title':_title, 'latitude':_coordinates.split(",").pop(), 'longitude':_coordinates.split(",")[0] })} /> })}
                <Flights transports={trip?.finFlight} notifyPressed={() => {}} />
            </div>
            <div className='display-map'>
                <GoogleMapsMap longitude={parseFloat(displayed.longitude)} latitude={parseFloat(displayed.latitude)} />
            </div>
        </div>
        {picIndex === -1 ? '': 
        <div className='display-images'>
            <button className='left-button' onClick={clickLeft}>&#60;</button>
            <button className='right-button' onClick={clickRight}>&#62;</button>
            <img className='image' src={picArray[picIndex]} />
            <button className='close-button' onClick={() => setPicIndex(-1)}>X</button>
        </div>}
    </div>
    )
}

DisplayTrip.propTypes = {
    trip: PropTypes.object.isRequired,
    canSort: PropTypes.bool,
    setEditedTrip: PropTypes.func
}