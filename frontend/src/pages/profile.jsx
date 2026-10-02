import { useEffect, useState } from "react";
import api from "../api";
import Navbar from "./Navbar";
import "../sytles/profile.css";
import { ACCESS_TOKEN } from '../constant';
import { jwtDecode } from "jwt-decode";

function Profile() {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {

        const getProfile = async () => {
            try {
                const token = localStorage.getItem(ACCESS_TOKEN);

                if (!token) {
                    setError("User is not logged in");
                    return;
                }

                const decoded = jwtDecode(token);
                const userID = decoded.userid;

                const response = await api.get(
                    `/api/userprofile/${userID}/`
                );

                setUser(response.data);

            } catch (error) {
                console.log(error.response?.data);

                setError(
                    error.response?.data?.detail ||
                    "Unable to load profile"
                );

            } finally {
                setLoading(false);
            }
        };

        getProfile();

    }, []);

    if (loading) {
        return <p>Loading profile...</p>;
    }

    if (error) {
        return <p>{error}</p>;
    }

    return (
        <>
            <Navbar />
                <div >
                <div className="profile-container">
                {/* Avatar / Header Section */}

                

                {/* Profile Form Details Section */}
                <div className="profile-details">
                    <div className="profile-detail">
                    <label>User ID</label>
                    <div className="input-field ">{user?.id || "1559 000 7788 8DER"}</div>
                    </div>

                    <div className="profile-detail">
                    <label>
                        Username <span className="required">*</span>
                    </label>
                    <div className="input-field">{user?.username || "John Doe"}</div>
                    </div>

                    <div className="profile-detail">
                    <label>Email</label>
                    <div className="input-field">{user?.email_id || "examples@gmail.com"}</div>
                    </div>

                    <div className="profile-detail">
                    <label>
                        Contact Number <span className="required">*</span>
                    </label>
                    <div className="input-field">
                        {user?.contact_number || "Not provided"}
                    </div>
                    </div>

                </div>

                
             </div>
             </div>
         </>
              )
            };

export default Profile;