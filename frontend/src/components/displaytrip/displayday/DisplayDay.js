import './DisplayDay.css';
import PropTypes from 'prop-types';
import DisplayActivity from './displayactivity/DisplayActivity';
import DisplayTransport from './displaytransport/DisplayTransport';
import { FaAvianex } from 'react-icons/fa';
import { useEffect, useRef, useState } from 'react';
import Sortable from 'sortablejs';


export default function DisplayDay({ day, index, iconPressed, notifyPressed, canSort, reportSorting }) {
    const sortActivities = useRef();
    const [ act_html, setActHtml ] = useState([]);
    const [ act_trans_joined, setActTransJoined ] = useState([]);

    // make activities sortable in needed
    let sortedActivities;
    useEffect(() => {
        if (typeof canSort !== 'undefined' && canSort) {
            sortedActivities = Sortable.create(sortActivities.current, {
                animation: 150,
                ghostClass: 'yellow-background-class',
                onUpdate: report
            });
    }}, [sortActivities]);

    useEffect(() => {
        setTimeout(() => {
            let activities = day?.activities;
            let transport = day?.transportation;
            
            let trans_html = []; // each cell is a display transportation element
            transport.map((trans, i) => {
                trans_html[i] = trans.map((tran, j) => { return <div className='fill-width' key={i.toString() + ',' + j.toString()}><DisplayTransport transport={tran} notifyPressed={notifyPressed} /></div>});
            });

            let html = [];
            activities.map((act, i) => { html[i] = <div className='fill-width' key={i} data-id={i}><DisplayActivity activity={act} iconPressed={iconPressed} notifyPressed={notifyPressed} /></div> });
            setActHtml([...html]);

            let i = 0;
            html = [];
            for (; i < activities.length; ++i) {
                html[2 * i] = trans_html[i];
                html[2 * i + 1] = act_html[i];
            }
            html[2 * i] = trans_html[i];
            setActTransJoined(html);
        })
    })

    if (typeof day === 'undefined') {
        return;
    }

    function report() {
        let sortedInts = [];
        sortedActivities.toArray().map((stringNum, i) => { sortedInts[i] = parseInt(stringNum); })
        reportSorting(sortedInts);
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
        <div className='pos' onClick={() => notifyPressed(pos?.title, pos?.destination)}>
            <div className='pos-row row-dash'>
                <div className='pos-row'>
                    <div className='pos-title'>{pos?.title}</div>
                    <div className='pos-pic' onClick={() => iconPressed(pos?.images)} color='blue'><FaAvianex /></div>
                    <a className='pos-link' href={pos?.link} target="_blank" rel="noopener noreferrer">link</a>
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