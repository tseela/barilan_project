import React, { useState } from 'react';
import './App.css';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom"
import { Home, Login } from "./pages"
import { UseToken } from "./components"

export default function App() {
  const { token, setToken } = UseToken();

  if(!token) {
    return <Login setToken={setToken} />
  }

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/home" element={<Home />} />
        <Route path="/login" element={<Login />} />
      </Routes>
    </Router>
  );
}

