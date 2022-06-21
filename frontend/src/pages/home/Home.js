import React from "react";
import './Home.css';
import { Navbar } from "../../components"
import { useToken } from "../../hooks";

export default function Home() {
    const { token, setToken } = useToken();

    return (
        <main className='home'>
            <header className='navbar'>
                <Navbar />
            </header>
            <div className="page-body">
                <div className="page">
                    <div className="text-left">
                        The <span>BEST</span> way to plan your trip is here!
                    </div>
                    <div className="text-right">
                        Having trouble planning your trip? We are here to help you!
                        <br></br>
                        <span className="logo-name"><span>T</span>rip<span>P</span>lanner</span> will plan the perfect trip especially for you.
                        <br></br>
                        We just need you to give us some information about your dream trip and we will be ready to go.
                        <br></br>
                        So... are you ready to begin?
                        <div className="start-div">
                            <a href="/plantrip" className="btn-start">start planning</a>
                        </div>
                    </div>
                </div>
                { token ? '' :  <div className="signup-section">
                    <a href="/signup" className="btn-signup">sign up</a>
                    <div className="signup-text">
                        you can sign up any time
                    </div>
                </div>
                }
            </div>
        </main>
    )
}

