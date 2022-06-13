import './ViewTrip.css';
import { useToken } from '../../hooks';
import { Forbidden } from '../index';
import { useState } from 'react';
import { Loading, Navbar } from '../../components';

export default function ViewTrip() {
    const { token, setToken } = useToken();
    const [ trip, setTrip ] = useState(null);
    const [ status, setStatus ] = useState(true); // true->all good, false->forbidden access

    if (!token || !status) {
        return(<Forbidden />);
    }

    if (status && !trip) {
        return(
            <div className='loading-container'>
                <Navbar />
                <div className='loading-div'>
                    <Loading />
                </div>
            </div>
        );
    }

    return(
        <div className='viewtrip'>

        </div>
    )
}