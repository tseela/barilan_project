import './GoogleMapsMap.css';
import PropTypes from 'prop-types';

/**
 * display map from google maps iframe given coordinates
 * 
 * @param latitude
 * @param longitude
 * @returns 
 */
export default function GoogleMapsMap({ latitude, longitude }) {
    // inject lat and long to link
    let mapLink = 'https://maps.google.com/maps?q=' + latitude + ',' + longitude + '&t=&z=13&ie=UTF8&iwloc=&output=embed';

    return(
    <div className="googlemaps-container">
        <iframe className='googlemaps' title='map' src={mapLink} loading="lazy" referrerPolicy="no-referrer-when-downgrade"></iframe>
    </div>
    )
}

GoogleMapsMap.propTypes = {
    latitude: PropTypes.number.isRequired,
    longitude: PropTypes.number.isRequired
}