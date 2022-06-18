import './GoogleMapsMap.css';
import PropTypes from 'prop-types';

export default function GoogleMapsMap({ latitude, longitude }) {
    if (typeof latitude === 'undefined' || typeof longitude === 'undefined') {
        return;
    }

    let mapLink = 'https://maps.google.com/maps?q=' + latitude + ',' + longitude + '&t=&z=13&ie=UTF8&iwloc=&output=embed';

    return(
    <div className="googlemaps-container">
        <iframe className='googlemaps' title='map' src={mapLink} loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
    </div>
    )
}

GoogleMapsMap.propTypes = {
    latitude: PropTypes.number,
    longitude: PropTypes.number
}