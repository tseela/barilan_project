import './App.css';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { Home, Login, SignUp, Profile, PageNotFound, ViewTrip } from "./pages";

export default function App() {
    return (
      <Router>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/home" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<SignUp />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/trip/:id" element={<ViewTrip />} />
          <Route path="*" element={<PageNotFound />} />
        </Routes>
      </Router>
    );
}

