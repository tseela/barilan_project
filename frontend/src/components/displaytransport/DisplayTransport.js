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

export default function DisplayTransport({ transport, notifyPressed }) {
    return(
    <div className="displaytransport-container" onClick={() => notifyPressed(transport?.title, transport?.googleMapsLink)}>
        <div className='trns-col'>
            <div className='trns-row row-dash'>
                <div className='trns-title'>
                    {transport?.title}<div className='trns-pic' color='blue'><FaAvianex /></div>
                </div>
            </div>
            <div className='trns-row row-dash'>
                <div className='trns-row'>
                    <div className='trns-time line'>
                        {getHour(transport?.timeStart)}{' => '}{getHour(transport?.timeEnd)}
                    </div>
                    <div className='trns-total trns-time'>
                        total: {transport?.duration}<span>hr</span>
                    </div>
                </div>
                <div className='trns-cost'>
                    cost: {transport?.cost}$
                </div>
            </div>
            <div className='trns-row row-dash'>
                <div className='trns-method trns-places'>
                    Take the {transport?.methodOfTransportation} from <span>{transport?.placeOfOrigin}</span> to <span>{transport?.destination}</span>
                </div>
            </div>
            <div className='trns-row row-dash'>
                <div className='trns-order'>
                    {transport?.orderInAdvance ? '*need to order reservation':''}
                </div>
            </div>
        </div>
    </div>
    )
}

DisplayTransport.propTypes = {
    transport: PropTypes.object.isRequired,
    notifyPressed: PropTypes.func
}