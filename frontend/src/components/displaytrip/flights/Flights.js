import './Flights.css';
import PropTypes from 'prop-types';

function removeSecondes(dateString) {
    return dateString.slice(0, -3);
}

export default function Flights({ transports, notifyPressed }) {
    return(
        <div className='flight-container'>
            <div className='flights-title row-dash'>
                Flight (with connections)
            </div>
    {transports.map((transport, index) => {
        return (
        <div key={index} className="flight-container">
            <div className='flight-col'>
                <div className='flight-row row-dash'>
                    <div className='align-left'>
                        <div className='flight-title'>Flight Code: {transport?.title.substr(2, transport?.title.length)}</div>
                        <div className='flight-title lil-margin'>Company: {transport?.title.substr(0, 2)}</div>
                        <div className='flight-title lil-margin' onClick={() => notifyPressed(transport?.baseStation, transport?.placeOfOrigin)}>{transport?.baseStation.slice(0, -2)}</div>
                        <div className='flight-title'>{' -> '}</div>
                        <div className='flight-title' onClick={() => notifyPressed(transport?.baseStation, transport?.destination)}>{transport?.arrivalStation}</div>
                    </div>
                </div>
                <div className='flight-row row-dash'>
                    <div className='flight-row'>
                        <div className='flight-time line'>
                            {removeSecondes(transport?.timeStart)}{' => '}{removeSecondes(transport?.timeEnd)}
                        </div>
                        <div className='flight-total flight-time'>
                            total: {transport?.duration.toFixed(2)}<span>hr</span>
                        </div>
                    </div>
                    {index === 0 ? <div className='flight-cost'>cost (including connections): {transport?.cost}$</div> : ''}
                </div>
                <div className='flight-row row-dash'>
                    <div className='flight-method flight-places flight-row'>
                        <div className='src-airport'>
                            Source Airport: <a className='flight-link' href={transport?.originLink} target="_blank" rel="noopener noreferrer">{transport?.baseStation.slice(0, -2)}</a>
                        </div>
                        <div className='flight-port'>
                            Terminal: {transport?.baseStation.split("-").pop()}
                        </div>
                        <div className='dest-airport'>
                            Destination Airport: <a className='flight-link' href={transport?.destinationLink} target="_blank" rel="noopener noreferrer">{transport?.arrivalStation}</a>
                        </div>
                    </div>
                </div>
                <div className='flight-row row-dash'>
                    <div className='flight-order'>
                        {transport?.orderInAdvance ? '*reservation required':''}
                    </div>
                </div>
            </div>
        </div>
        );
    })}
    </div>
    );
}

Flights.propTypes = {
    transports: PropTypes.array.isRequired, // array of flights
    notifyPressed: PropTypes.func
}