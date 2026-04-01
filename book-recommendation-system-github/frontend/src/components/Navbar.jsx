import { useNavigate } from "react-router-dom";
import { removeToken } from "../utils/auth";

export default function Navbar({ email }) {
  const navigate = useNavigate();

  const handleLogout = () => {
    removeToken();
    navigate("/login");
  };

  return (
    <div className="navbar">
      <h1>Book Recommendation System</h1>
      <div className="navbar-right">
        {email && <span>{email}</span>}
        <button onClick={handleLogout}>Logout</button>
      </div>
    </div>
  );
}