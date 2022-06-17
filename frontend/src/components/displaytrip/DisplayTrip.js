import './DisplayTrip.css';
import PropTypes from 'prop-types';
import DisplayDay from '../displayday/DisplayDay';
import { useRef, useState } from 'react';
import cloneDeep from 'lodash/cloneDeep';

export default function DisplayTrip({ trip, canSort, setEditedTrip }) {
    const [ displayed, setDisplayed ] = useState({ 'title':'', 'latitude':'32.0684408', 'longitude':'34.7740717' });
    const [ picArray, setPicArray ] = useState([]);
    const [ picIndex, setPicIndex ] = useState(-1);

    // after load, update editedTrip to be trip
    useRef(() => {
        if (canSort && typeof setEditedTrip !== 'undefined') {
            setEditedTrip(cloneDeep(trip));
        }
    }, []);

    let mapLink = "http://www.openstreetmap.org/export/embed.html?bbox=99.01707172393799%2C18.812250694616786%2C99.04603958129883%2C18.827077370495342&amp;layer=mapnik&amp;marker=18.819664196007352%2C99.03155565261841";

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
    // <iframe className='googlemaps' title='info' src={'https://maps.google.com/maps?q=' + parseFloat(displayed.latitude) + ',' + parseFloat(displayed.longitude) + '&t=&z=13&ie=UTF8&iwloc=&output=embed'}></iframe>
    return(
    <div className="displaytrip-container">
        <div className='reg-page-container' style={{opacity: picIndex === -1 ? 1 : 0.5}}>
            <div className='activities-display'>
                {trip?.days.map((d, i) => { return <DisplayDay reportSorting={(sortedInts) => report(sortedInts, i)} day={d} index={i} key={i} canSort={canSort} iconPressed={(img_array) => {setPicArray(img_array); setPicIndex(0);}} setEditedTrip={setEditedTrip} notifyPressed={(_title, _coordinates) => setDisplayed({ 'title':_title, 'latitude':_coordinates.split(",").pop(), 'longitude':_coordinates.split(",")[0] })} /> })}
            </div>
            <div className='displayitem'>
                <iframe className='googlemaps' title='info' src={mapLink}></iframe>
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