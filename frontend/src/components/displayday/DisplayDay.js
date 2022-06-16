import './DisplayDay.css';
import PropTypes from 'prop-types';
import DisplayActivity from '../displayactivity/DisplayActivity';
import DisplayTransport from '../displaytransport/DisplayTransport';
import { FaAvianex } from 'react-icons/fa';
import { useEffect, useRef } from 'react';
import Sortable from 'sortablejs';


export default function DisplayDay({ day, index, iconPressed, notifyPressed, canSort, reportSorting }) {
    const sortActivities = useRef();
    let sortedActivities;
    useEffect( () => {
        if (typeof canSort !== 'undefined' && canSort) {
            sortedActivities = Sortable.create(sortActivities.current, {
                animation: 150,
                ghostClass: 'yellow-background-class',
                onUpdate: report
            });
    }}, [sortActivities]);

    if (typeof day === 'undefined') {
        return;
    }

    function report() {
        let sortedInts = [];
        sortedActivities.toArray().map((stringNum, i) => { sortedInts[i] = parseInt(stringNum); })
        reportSorting(sortedInts);
    }

    let activities = day?.activities;
    let transport = day?.transportation;
    transport.push([]); // to make length equal to avtivities
    let trans_html = []; // each cell is a display transportation element
    transport.map((trans, i) => {
        trans_html[i] = trans.map((tran, j) => { return <DisplayTransport key={i.toString() + ',' + j.toString()} transport={tran} iconPressed={iconPressed} notifyPressed={notifyPressed} />});
    });

    let act_html = []; // each cell is a display activity element
    activities.map((act, i) => { act_html[i] = <DisplayActivity dataID={i.toString()} key={i} activity={act} iconPressed={iconPressed} notifyPressed={notifyPressed} /> });

    let act_trans_joined = [];  // each cell is a display element (ordered)
    for (let i = 0; i < activities.length; ++i) {
        act_trans_joined[2 * i] = act_html[i];
        act_trans_joined[2 * i + 1] = trans_html[i];
    }

    let pos = day?.placeOfStay;

    return(
    <div className="displayday-container">
        <div className='day-row'>
            <div className='day row-dash'>
                Day {index}
            </div>
            <div className='day-cost'>
                cost: {day?.cost}$
            </div>
        </div>
        <div className='pos' onClick={() => notifyPressed(pos?.title, pos?.googleMapsLink)}>
            <div className='pos-row row-dash'>
                <div className='pos-row'>
                    <div className='pos-title'>{pos?.title}</div>
                    <div className='pos-pic' onClick={() => iconPressed(pos?.googleMapsImageLink)} color='blue'><FaAvianex /></div>
                </div>
                <div className='pos-cost day-dash'>
                    cost: {pos?.cost}$
                </div>
            </div>
            <div className='pos-row row-dash'>
                <div className='pos-order'>
                    {pos?.orderInAdvance ? '*need to order reservation':''}
                </div>
            </div>
        </div>
        <div className='maybe-sorted' ref={sortActivities}>
            {canSort ? act_html.map((html) => { return html; }) 
                : act_trans_joined.map((html) => { return html; })}
        </div>
    </div>
    )
}

DisplayDay.propTypes = {
    day: PropTypes.object,
    index: PropTypes.number,
    iconPressed: PropTypes.func,
    canSort: PropTypes.bool,
    notifyPressed: PropTypes.func,
    reportSorting: PropTypes.func
}