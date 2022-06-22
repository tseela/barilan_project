import './DisplayTransport.css';
import PropTypes from 'prop-types';

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
    <div className="displaytransport-container">
        <div className='trns-col'>
            <div className='trns-row row-dash'>
                <div className='align-left'>
                    <div className='trns-title'>{transport?.title + ' | '}</div>
                    <div className='trns-title' onClick={() => notifyPressed(transport?.baseStation, transport?.placeOfOrigin)}>{transport?.baseStation}</div>
                    <div className='trns-title'>{' -> '}</div>
                    <div className='trns-title' onClick={() => notifyPressed(transport?.baseStation, transport?.destination)}>{transport?.arrivalStation}</div>
                </div>
            </div>
            <div className='trns-row row-dash'>
                <div className='trns-row'>
                    <div className='trns-time line'>
                        {getHour(transport?.timeStart)}{' => '}{getHour(transport?.timeEnd)}
                    </div>
                    <div className='trns-total trns-time'>
                        total: {parseFloat(transport?.duration).toFixed(2)}<span>hr</span>
                    </div>
                </div>
                <div className='trns-cost'>
                    cost: {transport?.cost}$
                </div>
            </div>
            <div className='trns-row row-dash'>
                <div className='trns-method trns-places'>
                    Take the {transport?.methodOfTransportation} from <a className='trns-link' href={transport?.originLink} target="_blank" rel="noopener noreferrer">{transport?.baseStation}</a> to <a className='trns-link' href={transport?.destinationLink} target="_blank" rel="noopener noreferrer">{transport?.arrivalStation}</a>
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