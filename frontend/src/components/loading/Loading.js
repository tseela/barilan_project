import './Loading.css';
import pic from './plane_loading.gif';

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