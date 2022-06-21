import './App.css';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { Home, Login, SignUp, Profile, PageNotFound, ViewTrip, EditTrip, PlanTrip } from "./pages";

export default function App() {
    return (
      <Router>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/home" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<SignUp />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/viewtrip/:id" element={<ViewTrip />} />
          <Route path="/edittrip/:id" element={<EditTrip />} />
          <Route path='/tripplanning' element={<PlanTrip />} />
          <Route path="*" element={<PageNotFound />} />
        </Routes>
      </Router>
    );
}

