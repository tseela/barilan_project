import PropTypes from 'prop-types';

export default function Logout({ setToken }) {
    return(
        <div>
            <button className='logout' onClick={() => setToken(null)}>Logout</button>
        </div>
    );
}

Logout.propTypes = {
    setToken: PropTypes.func.isRequired
}
