import './PlanTrip.css';
import { useToken } from '../../hooks';
import { OfflineEditTrip } from '../index';
import { useState, useEffect } from 'react';
import { Loading, Navbar, LoginDialog, SignUpDialog } from '../../components';
import Select from 'react-select';
import { Navigate } from 'react-router-dom';

// gets today's string
function getToday() {
    let today = new Date();
    let dd = String(today.getDate()).padStart(2, '0');
    let mm = String(today.getMonth() + 1).padStart(2, '0');
    let yyyy = today.getFullYear();

    return yyyy + '-' + mm + '-' + dd;
}

/**
 * plan/create trip page
 * 
 * @returns 
 */
export default function PlanTrip() {
    const { token, setToken } = useToken(); // user token
    const [ trip, setTrip ] = useState(null); // trip (initializes after created)
    const [ isLoading, setIsLoading ] = useState(false); // should show that the server is loading
    const [ shouldLogin, setShouldLogin ] = useState(false); // should login to user
    const [ isDone, setIsDone ] = useState(false); // navigate to different page when finished

    // non fail mechanizem
    const [ tryFetch, setTryFetch ] = useState(false); // try fetching maps again (probably after null returned)

    // checkboxes
    const [ isLuxuriance, setIsLuxuriance ] = useState(false);
    const [ isLowCost, setIsLowCost ] = useState(false);
    const [ isMuseumOriented, setIsMuseumOriented ] = useState(false);
    const [ isFastPaced, setIsFastPaced ] = useState(false);
    // more to fill
    const [ numOfPeople, setNumOfPeople ] = useState(1);
    const [ date, setDate ] = useState(getToday());
    const [ duration, setDuration ] = useState(3);
    const [ airport, setAirport ] = useState(null);
    const [ destination, setDestination ] = useState('');

    // flight and states-distrct array-maps
    const [ airportsMap, setAirportsMap ] = useState(undefined);
    const [ countriesMap, setCountriesMap ] = useState(undefined);
    const [ regionsMap, setRegionsMap ] = useState(undefined);
    const [ citiesMap, setCitiesMap ] = useState(undefined);
    // airports and regions options (options the user chooses from)
    const [ airportOptions, setAirportOptions ] = useState(undefined);
    const [ citiesOptions, setCitiesOptions ] = useState(undefined);

    // update options states
    function updateOptions() {
        if (typeof airportsMap === 'undefined') {
            return;
        }

        // element = { value: iata_code, label: Country, Region, Airport }
        let airports = [];
        for (let i = 0; i < airportsMap.length; ++i) {
            airports.push(
                { value : airportsMap[i]?.iata_code,
                    label : countriesMap.find(item => item?.code === airportsMap[i]?.iso_country).name + ', '
                     + regionsMap.find(item => item?.code === airportsMap[i]?.iso_region).name + ', '
                     + airportsMap[i]?.name
                });
        }
        setAirportOptions(airports);

        // element = { value: Region, label: Country, Region }
        let cities = [];
        for (let i = 0; i < citiesMap.length; ++i) {
            cities.push(
                { value : citiesMap[i]?.city,
                    label : citiesMap[i]?.country + ', ' + citiesMap[i]?.city
                });
        }
        setCitiesOptions(cities);
    }

    // get airport, countries and regions lists from backend server
    useEffect(() => {
        setIsLoading(true);
        fetch('getAirportsAndDistrictsLists', {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json'
            }}).then(res => res.json()).then((json) => {                
                setTimeout(() => {
                    setAirportsMap(json?.airportsMap);
                    setCountriesMap(json?.countriesMap);
                    setRegionsMap(json?.regionsMap);
                    setCitiesMap(json?.citiesMap)

                    updateOptions();

                    setIsLoading(false);
                }, 2000); // for cooldown
            });
    }, [tryFetch]); // sometimes, when the server is just starting json.airportsMap return undefined, tryFetch tells us to try fetching again

    // non fail mechanizem idea -> when map states gets updates, make sure they are not undefined
    useEffect(() => {
        if (typeof airportsMap === 'undefined') { // if undefined -> fetch again
            setTryFetch(!tryFetch);
        } else { // else, update options if needed and make sure we are not loading
            if (typeof airportOptions === 'undefined') {
                updateOptions();
            }
            setIsLoading(false);
        }
    }, [airportsMap]);

    // when loading, Select gets deleted but our state doesn't get nulled
    useEffect(() => setAirport(null), [isLoading]);

    const handleSubmit = async e => {
        e.preventDefault();
        // check validity
        if (airport === null) {
            alert("You must fill your closest airport!");
            return;
        } else if (isLuxuriance === true && isLowCost == true) {
            alert("Yout trip can't be both luxuriance and low-cost!");
            return;
        }

        // ask for a new trip
        setIsLoading(true);
        fetch('createTrip', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            }, body: JSON.stringify({
                'numOfPeople' : numOfPeople,
                'startDate' : date,
                'duration' : duration,
                'srcAirport' : airport,
                'destination' : destination,
                'flags': {
                    'isFastPaced' : isFastPaced,
                    'isMuseumOriented' : isMuseumOriented,
                    'isLuxuriance' : isLuxuriance,
                    'isLowCost' : isLowCost
                }
            })}).then((res) => {
                if (res.status === 200) {
                    return res.json();
                }
                alert("Could not find a matching flight.")
                return null;
            }).then((res) => {
                setTrip(res);
                setIsLoading(false);
            })
    }

    // ask backend to save the trip
    function saveTrip(tripToSave) {
        if (!token) {
            alert("You need to login first!");
            setShouldLogin(true);
        } else {
            fetch('/insertTripToUser', {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json'
                },
                body: JSON.stringify({'token':token, 'trip':tripToSave})
            }).then((res) => {
                if (res.status === 200) {
                    alert("Success! Trip saved.");
                    setIsDone(true);
                } else {
                    alert("Something went wrong... Your trip couldn't be saved.\nTry again in a few seconds.");
                }
            });
        }
    }

    if (isDone) { // goto profile
        return(<Navigate to="/profile" />);
    }

    if (isLoading) { // loading screen
        return(
            <div className='plantrip-container'>
                <Navbar />
                <div className='loading-div'>
                    <Loading />
                </div>
            </div>
        );
    }

    if (!token && shouldLogin) { // connect to user screen
        return(
            <div className='plantrip-container'>
                <Navbar />
                <div className='delayed-login-div'>
                    <div className='delayed-login dialog'><LoginDialog setToken={setToken} directToRegister={false} /></div>
                    <div className='delayed-signup dialog'><SignUpDialog alertSignUp={() => {}} directToLogin={false} /></div>
                </div>
            </div>
        );
    }

    if (!trip) { // create trip screen
        return(
            <div className='re-render'> {/* needed after login from this url */}
                <div className='plantrip-container'>
                    <Navbar />
                    <div className='createtrip'>
                        {/* some text */}
                        <div className='create-text'>
                            <div className='create-headline'>Create a new trip:</div>
                            <div className='create-body'>Mark below the details about the trip you whould like to go on and we will find you your dream trip right away!</div>
                        </div>
                        <form onSubmit={handleSubmit} className='createtrip-form'>
                            <div className='row'>
                                <div className='left'>
                                    <label>Number of Passengers:</label>
                                    <input type="number" min={1} placeholder={1} onChange={(e) => setNumOfPeople(parseInt(e.target.value))} />
                                    <br></br>
                                    <label>Start Date:</label>
                                    <input type="date" onChange={(e) => setDate(e.target.value)} />
                                    <br></br>
                                    <label>Trip Duration (in days):</label>
                                    <input type="number" min={3} placeholder={2} onChange={(e) => setDuration(parseInt(e.target.value) + 1)} />
                                    <p></p>
                                    <label>Your Closest Airport:</label>
                                    <div className='font-smaller'><Select options={airportOptions} onChange={(e) => setAirport(e.value)} /></div>
                                    <br></br>
                                    <label>Desired Destination:</label>
                                    <div className='font-smaller'><Select options={citiesOptions} onChange={(e) => setDestination(e.value)} /></div>
                                    <br></br>
                                </div>
                                <div className='right'>
                                    <input type="checkbox" onChange={() => setIsLuxuriance(!isLuxuriance)} />
                                    <label>Luxury trip</label>
                                    <br></br>
                                    <input type="checkbox" onChange={() => setIsLowCost(!isLowCost)} />
                                    <label>Low-cost trip</label>
                                    <br></br>
                                    <input type="checkbox" onChange={() => setIsMuseumOriented(!isMuseumOriented)} />
                                    <label>Museum Oriented</label>
                                    <br></br>
                                    <input type="checkbox" onChange={() => setIsFastPaced(!isFastPaced)} />
                                    <label>Fast Paced</label>
                                    <br></br>
                                </div>
                            </div>
                            <div className='createtrip-btn-div'><button className='createtrip-btn' type="submit">Generate Trip</button></div>
                        </form>
                    </div>
                </div>
            </div>
        );
    }

    if (trip) { // trip is set -> display it
        return(<OfflineEditTrip trip={trip} saveEditedTrip={saveTrip} canCancel={false} />);
    }
}