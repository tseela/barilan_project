import './Loading.css';
import pic from './plane_loading.gif';

/**
 * loading gif and animation
 * 
 * @returns 
 */
export default function Loading() {
    return(
    <div className="loading">
        {/* plane flying gif */}
        <img src={pic} className="pic" alt="Loading" />
        <div className='loading-text'>
            <div>
                Loading
            </div>
            {/* loading animation */}
            <div className='loader'></div>
        </div>
    </div>
    )
}