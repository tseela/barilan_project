import './DisplayTransport.css';
import PropTypes from 'prop-types';
import { FaAvianex } from 'react-icons/fa';

// get full date and return just hours and mins
function getHour(date) {
    let i = date.indexOf(':') - 2;
    if (i < 0) {
        return '';
    }
    return date.substring(i, i + 5);
}

export default function DisplayTransport({ transport }) {
    function nothing() {

    }
    return(
    <div className="displaytransport-container">
        <div className='trns-col'>
            <div className='trns-row'>
                <div className='trns-title'>{transport?.title}</div>
                <div className='trns-pic' onClick={nothing} color='blue'><FaAvianex /></div>
            </div>
            <div className='trns-row'>
                <div className='time line'>
                    {getHour(transport?.timeStart)}{' => '}{getHour(transport?.timeEnd)}
                </div>
                <div className='total time'>
                    total: {transport?.duration}<span>hr</span>
                </div>
                <div className='cost dash'>
                    cost: {transport?.cost}$
                </div>
            </div>
            <div className='trns-row'>
                <div className='order'>
                    {transport?.orderInAdvance ? '*need to order reservation':''}
                </div>
            </div>
        </div>
    </div>
    )
}

DisplayTransport.propTypes = {
    transport: PropTypes.object.isRequired
}