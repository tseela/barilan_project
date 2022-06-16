import './DisplayActivity.css';
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

// display one activity
export default function DisplayActivity({ activity, iconPressed, notifyPressed, dataID }) {
    if (!activity) {
        return;
    }

    return(
    <div className="displayactivity-container" data-id={dataID} onClick={() => notifyPressed(activity?.title, activity?.googleMapsLink)}>
        <div className='act-col'>
            <div className='act-row row-dash'>
                <div className='act-title'>
                    {activity?.title}
                    <div className='act-pic' onClick={() => iconPressed(activity?.googleMapsImageLink)} color='blue'><FaAvianex /></div>
                </div>
            </div>
            <div className='act-row row-dash'>
                <div className='act-row'>
                    <div className='act-time line'>
                        {getHour(activity?.timeStart)}{' => '}{getHour(activity?.timeEnd)}
                    </div>
                    <div className='act-total act-time'>
                        total: {activity?.duration}<span>hr</span>
                    </div>
                </div>
                <div className='act-cost'>
                    cost: {activity?.cost}$
                </div>
            </div>
            <div className='act-row row-dash'>
                <div className='act-order'>
                    {activity?.orderInAdvance ? '*need to order reservation':''}
                </div>
            </div>
        </div>
    </div>
    )
}

DisplayActivity.propTypes = {
    activity: PropTypes.object,
    iconPressed: PropTypes.func,
    notifyPressed: PropTypes.func,
    dataID: PropTypes.string
}