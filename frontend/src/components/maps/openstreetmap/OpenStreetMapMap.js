import './OpenStreetMapMap.css';
import PropTypes from 'prop-types';
import { map } from 'lodash';

export default function OpenStreetMapMap({ latitude, longitude, scale }) {
    if (typeof latitude === 'undefined' || typeof longitude === 'undefined') {
        return;
    }

    let fixedScale = scale;
    if (typeof scale === 'undefined') {
        fixedScale = 0.008;
    }

    let long1 = Number((longitude - fixedScale).toFixed(6));
    let lat1 = Number((latitude - fixedScale).toFixed(6));
    let long2 = Number((longitude + fixedScale).toFixed(6));
    let lat2 = Number((latitude + fixedScale).toFixed(6));

    let bbox = long1 + ',' + lat1 + ',' + long2 + ',' + lat2;
    let marker = Number((latitude).toFixed(6)) + ',' + Number((longitude).toFixed(6));

    let mapLink = 'http://www.openstreetmap.org/export/embed.html?bbox=' + bbox + '&amp;layer=mapnik&amp;marker=' + marker;

    return(
    <div className="openstreetmap-container">
        <iframe className='openstreetmap' title='map' src={mapLink}></iframe>
        <br/>
        <small><a className='bigger-link' target="_blank" rel="noopener noreferrer" href={'https://www.openstreetmap.org/?mlat=' + latitude + '&amp;mlon=' + longitude + '#map=15/' + latitude + '/' + longitude}>צפייה במפה גדולה יותר</a></small>
    </div>
    )
}

OpenStreetMapMap.propTypes = {
    latitude: PropTypes.number,
    longitude: PropTypes.number,
    scale: PropTypes.number
}