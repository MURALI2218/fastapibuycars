import api from  "../api";
import Navbar from "./Navbar";
import { useState, useEffect } from "react";
import  '../sytles/booking.css'

function Bookings(){
    const [datafromapi, setDatas] =useState("")
    const [loading, setLoading] = useState(true);
        
            const fetchCars = () => {

                setLoading(true);

                setTimeout(() => {

                    api.get("/api/carbooking/")
                        .then((response) => {
                            setDatas(response.data);
                        })
                        .catch((error) => {
                            console.log(error.message);
                            setError(error.message);
                        })
                        .finally(() => {
                            setLoading(false);
                        });

                }, 1000);
            };

        useEffect(() => {
            fetchCars();
        }, []);

        const handlebookdeletebtn = (() => (
            pass
        )
        );

    return(
        <>
         <Navbar></Navbar>
         {loading ? (
            <div className="cars-loading">
                    <div className="spinner"></div>
                    <p>Loading Bookings...</p>
                </div>
         ):(
            <div>
                <h1>Your Booked Cars to Buy</h1>
               <h2 className="section-title">
                Cars
                <span className="car-count">
                   total - {datafromapi.length} cars
                </span>
            </h2>

            <div className="table-responsive">
  <table className="cars-table">
    <thead>
      <tr>
        <th>Customer</th>
        <th>Customer Contact</th>
        <th>Car Model</th>
        <th>Price</th>
        <th>Owner Name</th>
        <th>Owner Contact</th>
        <th>Gear Type</th>
        <th>Fuel Type</th>
        <th>Location</th>
        <th>Actions</th>
      </tr>
    </thead>
    <tbody>
      {datafromapi.map((booking) => (
        <tr key={booking.bookingid}>
          <td>{booking.name}</td>
          <td>{booking.contact_number}</td>
          <td>
            {booking.car.brand.brand} {booking.car.model}
          </td>
          <td className="price-cell">₹{booking.car.price}</td>
          <td>{booking.car.owner.username}</td>
          <td>{booking.car.owner.contact_number}</td>
          <td>{booking.car.geartype.geartype}</td>
          <td>{booking.car.fueltype.fueltype}</td>
          <td>{booking.car.carlocation}</td>
          <td>
            <button
              className="btn btn-delete"
              onClick={() => handlebookdeletebtn()}
            >
              Delete Booking
            </button>
          </td>
        </tr>
      ))}
    </tbody>
  </table>
</div>
            </div>
         )
        }
        </>
   
    )
}

export default Bookings

 
       
        

            
                
       