import './OpenStreetMapMap.css';
import PropTypes from 'prop-types';

/**
 * display map from open-street-map iframe given coordinates
 * 
 *      PROBLEM - doesn't show marker (because of open-street-map problem, my code is great)
 * 
 * @param latitude
 * @param longitude
 * @param scale - zoom on map
 * @returns 
 */
export default function OpenStreetMapMap({ latitude, longitude, scale=0.008 }) {
    // build a rectangle with coordinates
    /**
     *             lat1
     *       |‾‾‾‾‾‾‾‾‾‾‾‾‾‾|
     * long1 |              | long2
     *       |______________|
     *             lat2
     */
    let long1 = Number((longitude - scale).toFixed(6));
    let lat1 = Number((latitude - scale).toFixed(6));
    let long2 = Number((longitude + scale).toFixed(6));
    let lat2 = Number((latitude + scale).toFixed(6));

    let bbox = long1 + ',' + lat1 + ',' + long2 + ',' + lat2;
    let marker = Number((latitude).toFixed(6)) + ',' + Number((longitude).toFixed(6));

    let mapLink = 'http://www.openstreetmap.org/export/embed.html?bbox=' + bbox + '&amp;layer=mapnik&amp;marker=' + marker;

    return(
    <div className="openstreetmap-container">
        <iframe className='openstreetmap' title='map' src={mapLink}></iframe>
        <br/>
        {/* credit */}
        <small><a className='bigger-link' target="_blank" rel="noopener noreferrer" href={'https://www.openstreetmap.org/?mlat=' + latitude + '&amp;mlon=' + longitude + '#map=15/' + latitude + '/' + longitude}>צפייה במפה גדולה יותר</a></small>
    </div>
    )
}

OpenStreetMapMap.propTypes = {
    latitude: PropTypes.number.isRequired,
    longitude: PropTypes.number.isRequired,
    scale: PropTypes.number
}