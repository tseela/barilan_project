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
export default function DisplayActivity({ activity, iconPressed }) {
    return(
    <div className="displayactivity-container">
        <div className='act-col'>
            <div className='act-row'>
                <div className='act-title'>{activity?.title}</div>
                <div className='act-pic' onClick={iconPressed} color='blue'><FaAvianex /></div>
            </div>
            <div className='act-row'>
                <div className='time line'>
                    {getHour(activity?.timeStart)}{' => '}{getHour(activity?.timeEnd)}
                </div>
                <div className='total time'>
                    total: {activity?.duration}<span>hr</span>
                </div>
                <div className='cost dash'>
                    cost: {activity?.cost}$
                </div>
            </div>
            <div className='act-row'>
                <div className='order'>
                    {activity?.orderInAdvance ? '*need to order reservation':''}
                </div>
            </div>
        </div>
    </div>
    )
}

DisplayActivity.propTypes = {
    activity: PropTypes.object.isRequired,
    iconPressed: PropTypes.func.isRequired
}