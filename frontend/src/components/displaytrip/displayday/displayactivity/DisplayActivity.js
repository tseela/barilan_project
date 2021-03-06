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

/**
 * displays a single activity
 * 
 * @param activity
 * @param iconPressed - notify that images icon is pressed
 * @param notifyPressed - notify that coordinate should be displayed
 * @returns 
 */
export default function DisplayActivity({ activity, iconPressed, notifyPressed }) {
    return(
    <div className="displayactivity-container" onClick={() => notifyPressed(activity?.title, activity?.destination)}>
        <div className='act-col'>
            <div className='act-row row-dash'>
                {/* title */}
                <div className='act-title'>
                    {activity?.title}
                    <div className='act-pic' onClick={() => iconPressed(activity?.images)} color='blue'><FaAvianex /></div>
                </div>
            </div>
            <div className='act-row row-dash'>
                {/* times and cost */}
                <div className='act-row'>
                    <div className='act-time line'>
                        {getHour(activity?.timeStart)}{' => '}{getHour(activity?.timeEnd)}
                    </div>
                    <div className='act-total act-time'>
                        total: {activity?.duration.toFixed(2)}<span>hr</span>
                    </div>
                    <a className='act-link' href={activity?.link} target="_blank" rel="noopener noreferrer">link</a>
                </div>
                <div className='act-cost'>
                    cost: {activity?.cost}$
                </div>
            </div>
            <div className='act-row row-dash'>
                {/* order in advance (only if needed) */}
                <div className='act-order'>
                    {activity?.orderInAdvance ? '*need to order reservation':''}
                </div>
            </div>
        </div>
    </div>
    )
}

DisplayActivity.propTypes = {
    activity: PropTypes.object.isRequired,
    iconPressed: PropTypes.func,
    notifyPressed: PropTypes.func
}