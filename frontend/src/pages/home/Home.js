import React from "react";
import './Home.css';
import {Navbar} from "../../components"

export default function Home() {
    return (
        <main className='page'>
            <header className='header'>
                <Navbar />
            </header>
        </main>
    )
}

