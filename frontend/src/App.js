import './App.css';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { Home, SignIn, Profile } from "./pages";

export default function App() {
    return (
      <Router>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/home" element={<Home />} />
          <Route path="/signin" element={<SignIn />} />
          <Route path="/profile" element={<Profile />} />
        </Routes>
      </Router>
    );
}

