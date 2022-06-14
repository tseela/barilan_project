import './DisplayDay.css';
import PropTypes from 'prop-types';

// get full date and return just hours and mins
function getHour(date) {
    let i = date.indexOf(':') - 2;
    if (i < 0) {
        return '';
    }
    return date.substring(i, i + 5);
}

export default function DisplayDay({ day }) {
    return(
    <div className="displayday-container">
        
    </div>
    )
}

DisplayDay.propTypes = {
    day: PropTypes.object.isRequired
}