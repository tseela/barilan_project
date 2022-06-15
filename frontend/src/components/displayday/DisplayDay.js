import './DisplayDay.css';
import PropTypes from 'prop-types';
import DisplayActivity from '../displayactivity/DisplayActivity';
import DisplayTransport from '../displaytransport/DisplayTransport';
import { FaAvianex } from 'react-icons/fa';

/**
 * 'cost' : 123,
    'duration' : 1.5,
    'timeStart' : datetime.now(),
    'timeEnd' : datetime.now(),
    'placeOfStay' : {
                'cost' : 50,
                'destination' : 'Israel',
                'duration' : 1,
                'googleMapsImageLink' : ['https://www.danhotels.co.il/sites/default/files/styles/full_page_3_8/public/2018-08/DTGallery1.jpg?itok=0_WynAai'],
                'googleMapsLink' : ['https://www.google.co.il/travel/hotels/entity/CgsI74CAlc6F1erQARAB?g2lb=2502405%2C2502548%2C4208993%2C4254308%2C4258168%2C4260007%2C4270442%2C4271060%2C4274032%2C4285990%2C4288513%2C4289525%2C4291318%2C4296668%2C4301054%2C4302823%2C4305595%2C4308216%2C4313006%2C4314836%2C4315873%2C4317816%2C4317915%2C4324289%2C4329288%2C4329495%2C4333234%2C4270859%2C4284970%2C4291517%2C4292955%2C4316256%2C4333106&hl=iw&gl=il&un=1&rp=EPOJxP-ega-d9QE4AUAASAE&ictx=1&sa=X&tcfs=EhoaGAoKMjAxOS0xMS0yNxIKMjAxOS0xMS0yOFIA&utm_campaign=sharing&utm_medium=link&utm_source=htls&ts=CAESABp9Cl8SWzIlMHgxNTFlYTBmNTEzZDk0ZDBiOjB4ZjUzYWJjMDllZmYxMDRmMzoy15DXptecINeQ157Xmdeo15Qg15XXkifXldeo15InINeX15PXqNeZINeQ15nXqNeV15caABIaEhQKBwjmDxAIGBsSBwjmDxAIGBwYATICEAAqCwoHKAE6A0lMUxoA&ap=iAEC&ved=0CAAQ5JsGahcKEwiQ4s3y9an4AhUAAAAAHQAAAAAQAw'],
                'orderInAdvance' : True,
                'title' : 'DAN Hotel'
            }
 */
export default function DisplayDay({ day, index, iconPressed, notifyPressed, canSort, setEditedTrip }) {
    if (!day) {
        return;
    }

    let activities = day?.activities;
    let transport = day?.transportation;
    transport.push([]); // to make length equal to avtivities
    let trans_html = []; // each cell is a display transportation element
    transport.map((trans, i) => {
        trans_html[i] = trans.map((tran, j) => { return <DisplayTransport key={i.toString() + ',' + j.toString()} transport={tran} notifyPressed={notifyPressed} />});
    });

    let act_html = []; // each cell is a display activity element
    activities.map((act, i) => { act_html[i] = <DisplayActivity key={i} activity={act} notifyPressed={notifyPressed} /> });

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
                    <div className='pos-pic' onClick={iconPressed} color='blue'><FaAvianex /></div>
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
        <div className='maybe-sorted'>
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
    setEditedTrip: PropTypes.func,
    notifyPressed: PropTypes.func
}