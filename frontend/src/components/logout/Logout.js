import PropTypes from 'prop-types';

export default function Logout({ setToken }) {
    return(
        <div>
            <button onClick={() => setToken(null)}>Logout from account</button>
        </div>
    );
}

Logout.propTypes = {
    setToken: PropTypes.func.isRequired
}
