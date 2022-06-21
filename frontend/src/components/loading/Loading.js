import './Loading.css';
import pic from './plane_loading.gif';

// show user we are loading data
export default function Loading() {
    return(
    <div className="loading">
        <img src={pic} className="pic" alt="Loading" />
        <div className='loading-text'>
            <div>
                Loading
            </div>
            <div className='loader'></div>
        </div>
    </div>
    )
}