import './DisplayDay.css';
import PropTypes from 'prop-types';
import DisplayActivity from './displayactivity/DisplayActivity';
import DisplayTransport from './displaytransport/DisplayTransport';
import { FaAvianex } from 'react-icons/fa';
import { useEffect, useRef, useState } from 'react';
import Sortable from 'sortablejs';

/**
 * displays a single day (activities & transport)
 * 
 * @param day
 * @param index - num of day (display in block title)
 * @param iconPressed - notify that images icon is pressed
 * @param notifyPressed - notify that coordinate should be displayed
 * @param canSort - if the activities can be sorted
 * @param reportSorting - when sort change -> report about the change
 * @returns 
 */
export default function DisplayDay({ day, index, iconPressed, notifyPressed, canSort, reportSorting }) {
    const sortActivities = useRef();
    const [ act_html, setActHtml ] = useState([]); // html array of all activities
    const [ act_trans_joined, setActTransJoined ] = useState([]); // html array of all activities and transport ordered by time stamps

    // make activities sortable if needed
    let sortedActivities;
    useEffect(() => {
        if (typeof canSort !== 'undefined' && canSort) {
            sortedActivities = Sortable.create(sortActivities.current, {
                animation: 150,
                ghostClass: 'yellow-background-class',
                onUpdate: report
            });
    }}, [sortActivities]);

    // initialize act_html and act_trans_joined states
    // it's in useEffect because the changes update after rendering returns
    useEffect(() => {
        setTimeout(() => {
            let activities = day?.activities;
            let transport = day?.transportation;
            
            let trans_html = []; // each cell is a display transportation element
            if (transport) {
                transport.map((trans, i) => {
                    trans_html[i] = trans.map((tran, j) => { return <div className='fill-width' key={i.toString() + ',' + j.toString()}><DisplayTransport transport={tran} notifyPressed={notifyPressed} /></div>});
                });
            }

            let html = [];
            activities.map((act, i) => { html[i] = <div className='fill-width' key={i} data-id={i}><DisplayActivity activity={act} iconPressed={iconPressed} notifyPressed={notifyPressed} /></div> });
            setActHtml([...html]);

            // join lists
            let i = 0;
            html = [];
            for (; i < activities.length; ++i) {
                html[2 * i] = trans_html[i];
                html[2 * i + 1] = act_html[i];
            }
            html[2 * i] = trans_html[i];
            setActTransJoined([...html]);
        }, 500);
    })

    if (typeof day === 'undefined') {
        return;
    }

    // report sorting -> turn sortedActivities into array where val = index of activity from original trip
    function report() {
        let sortedInts = [];
        sortedActivities.toArray().map((stringNum, i) => { sortedInts[i] = parseInt(stringNum); })
        reportSorting(sortedInts);
    }

    let pos = day?.placeOfStay;

    return(
    <div className="displayday-container">
        <div className='day-row'>
            {/* title box */}
            <div className='day row-dash'>
                Day {index}
            </div>
            <div className='day-cost'>
                cost: {day?.cost}$
            </div>
        </div>
        {/* place of stay display */}
        <div className='pos' onClick={() => notifyPressed(pos?.title, pos?.destination)}>
            <div className='pos-row row-dash'>
                <div className='pos-row'>
                    {/* title */}
                    <div className='pos-title'>{pos?.title}</div>
                    <div className='pos-pic' onClick={() => iconPressed(pos?.images)} color='blue'><FaAvianex /></div>
                    <a className='pos-link' href={pos?.link} target="_blank" rel="noopener noreferrer">link</a>
                </div>
                {/* cost */}
                <div className='pos-cost day-dash'>
                    cost: {pos?.cost}$
                </div>
            </div>
            <div className='pos-row row-dash'>
                {/* order if needed */}
                <div className='pos-order'>
                    {pos?.orderInAdvance ? '*need to order reservation':''}
                </div>
            </div>
        </div>
        {/* display activities and transport by timestamps order */}
        {/* if canSort -> display only activities (transport should by updated by backend) */}
        <div className='maybe-sorted' ref={sortActivities}>
            {canSort ? act_html.map((html) => { return html; }) 
                : act_trans_joined.map((html) => { return html; })}
        </div>
    </div>
    )
}

DisplayDay.propTypes = {
    day: PropTypes.object.isRequired,
    index: PropTypes.number,
    iconPressed: PropTypes.func,
    canSort: PropTypes.bool,
    notifyPressed: PropTypes.func,
    reportSorting: PropTypes.func
}