import { useState, useEffect, filter } from "react";
import api from  "../api";
import Navbar from "./Navbar";
import '../sytles/createcarform.css';
import '../sytles/chatbot.css'
import '../sytles/home.css'

function Home(){
    

    const [datafromapi, setDatas] = useState([]);
const [error, setError] = useState(false);

const [searchModel, setSearchModel] = useState("");
const [selectedCity, setSelectedCity] = useState("");
const [selectedFuel, setSelectedFuel] = useState("");
const [selectedGear, setSelectedGear] = useState("");
const [selectedBudget, setSelectedBudget] = useState("");
const [selectedColour, setSelectedColour] = useState("");
const [selectedYear, setSelectedYear] = useState("");

const [activeFilter, setActiveFilter] = useState(null);
const [showAllFilters, setShowAllFilters] = useState(false);
    
    const chatOpen = true
    //Function For Fetching DATA from BACKEND
    const fetchCars = () =>{
                
                    setTimeout( ()=> {
                        api.get('/api/cars/')
                            .then( (response) =>{return response.data})
                            .then( (data) => {setDatas(data);})
                            .catch( (error) => {console.log(error.message);setError(error.message);
                            })
                    });
              
                return [datafromapi, error]
            }
             //Call function for fetch CARS from database
           useEffect(() => {
                fetchCars();
                }, []);


                //FLITERS
                const filteredCars = datafromapi.filter((car) => {

    const modelMatch =
        searchModel === "" ||
        car.model.toLowerCase().includes(searchModel.toLowerCase());

    const cityMatch =
        selectedCity === "" ||
        car.carlocation.toLowerCase() === selectedCity.toLowerCase();

    const fuelMatch =
        selectedFuel === "" ||
        car.fueltype?.fueltype.toLowerCase() === selectedFuel.toLowerCase();

    const gearMatch =
        selectedGear === "" ||
        car.geartype?.geartype.toLowerCase() === selectedGear.toLowerCase();

    const colourMatch =
        selectedColour === "" ||
        car.colour.toLowerCase() === selectedColour.toLowerCase();

    const yearMatch =
        selectedYear === "" ||
        String(car.year) === selectedYear;

    let budgetMatch = true;

    if (selectedBudget === "Under 5 Lakhs") {
        budgetMatch = Number(car.price) < 500000;
    }

    if (selectedBudget === "5 - 10 Lakhs") {
        budgetMatch =
            Number(car.price) >= 500000 &&
            Number(car.price) <= 1000000;
    }

    if (selectedBudget === "10 - 20 Lakhs") {
        budgetMatch =
            Number(car.price) > 1000000 &&
            Number(car.price) <= 2000000;
    }

    if (selectedBudget === "Above 20 Lakhs") {
        budgetMatch = Number(car.price) > 2000000;
    }

    return (
        modelMatch &&
        cityMatch &&
        fuelMatch &&
        gearMatch &&
        colourMatch &&
        yearMatch &&
        budgetMatch
    );
});

               return(
                <>
                    <Navbar></Navbar>
                    
        {/* FILTER SECTION */}
        <div className="car-filter-section">

            <div className="filter-top">
                <h2>Find Your Right Car</h2>
            </div>


            {/* SEARCH BAR */}
                <div className="search-section">
            <div className="car-search-box">
                     <input
                    type="text"
                    placeholder="Type to car model ex. Punch"
                    value={searchModel}
                    onChange={(e) =>
                        setSearchModel(e.target.value)
                    }
                />
                <i className="bi bi-search search-icon"></i>
                </div>
               

            {/* FILTER BUTTONS */}

            <div className="filter-buttons">

                {/* BUDGET */}

                <div className="filter-wrapper">

                    <button
                        className={`filter-button ${
                            activeFilter === "budget"
                                ? "filter-active"
                                : ""
                        }`}
                        onClick={() =>
                            setActiveFilter(
                                activeFilter === "budget"
                                    ? null
                                    : "budget"
                            )
                        }
                    >
                        <i className="bi bi-cash-stack"></i>
                        Budget
                    </button>

                    {activeFilter === "budget" && (
                        <div className="filter-dropdown">

                            <button onClick={() => {
                                setSelectedBudget("");
                                setActiveFilter(null);
                            }}>
                                Any Budget
                            </button>

                            <button onClick={() => {
                                setSelectedBudget("Under 5 Lakhs");
                                setActiveFilter(null);
                            }}>
                                Under ₹5 Lakhs
                            </button>

                            <button onClick={() => {
                                setSelectedBudget("5 - 10 Lakhs");
                                setActiveFilter(null);
                            }}>
                                ₹5 - ₹10 Lakhs
                            </button>

                            <button onClick={() => {
                                setSelectedBudget("10 - 20 Lakhs");
                                setActiveFilter(null);
                            }}>
                                ₹10 - ₹20 Lakhs
                            </button>

                            <button onClick={() => {
                                setSelectedBudget("Above 20 Lakhs");
                                setActiveFilter(null);
                            }}>
                                Above ₹20 Lakhs
                            </button>

                        </div>
                    )}

                </div>

                {/* FUEL */}

                <div className="filter-wrapper">

                    <button
                        className="filter-button"
                        onClick={() =>
                            setActiveFilter(
                                activeFilter === "fuel"
                                    ? null
                                    : "fuel"
                            )
                        }
                    >
                        <i className="bi bi-fuel-pump"></i>
                        Fuel Type
                    </button>

                    {activeFilter === "fuel" && (
                        <div className="filter-dropdown">

                            <button onClick={() => {
                                setSelectedFuel("");
                                setActiveFilter(null);
                            }}>
                                All Fuel Types
                            </button>

                            <button onClick={() => {
                                setSelectedFuel("Petrol");
                                setActiveFilter(null);
                            }}>
                                Petrol
                            </button>

                            <button onClick={() => {
                                setSelectedFuel("Diesel");
                                setActiveFilter(null);
                            }}>
                                Diesel
                            </button>

                            <button onClick={() => {
                                setSelectedFuel("Electric");
                                setActiveFilter(null);
                            }}>
                                Electric
                            </button>

                            <button onClick={() => {
                                setSelectedFuel("CNG");
                                setActiveFilter(null);
                            }}>
                                CNG
                            </button>

                        </div>
                    )}

                </div>


                {/* TRANSMISSION */}

                <div className="filter-wrapper">

                    <button
                        className="filter-button"
                        onClick={() =>
                            setActiveFilter(
                                activeFilter === "gear"
                                    ? null
                                    : "gear"
                            )
                        }
                    >
                        <i className="bi bi-gear"></i>
                        Transmission
                    </button>

                    {activeFilter === "gear" && (
                        <div className="filter-dropdown">

                            <button onClick={() => {
                                setSelectedGear("");
                                setActiveFilter(null);
                            }}>
                                All
                            </button>

                            <button onClick={() => {
                                setSelectedGear("Manual");
                                setActiveFilter(null);
                            }}>
                                Manual
                            </button>

                            <button onClick={() => {
                                setSelectedGear("Automatic");
                                setActiveFilter(null);
                            }}>
                                Automatic
                            </button>

                        </div>
                    )}

                </div>

                  
                     <div className="filter-wrapper">
                       
                        <select
                            value={selectedColour}
                            onChange={(e) =>
                                setSelectedColour(e.target.value)
                            }
                        >
                            <option value="">All Colours</option>

                            {[...new Set(
                                datafromapi.map(car => car.colour)
                            )].map(colour => (
                                <option
                                    key={colour}
                                    value={colour}
                                >
                                    {colour}
                                </option>
                            ))}

                        </select>
                            </div>

                            
                    <div className="filter-wrapper">

                       

                        <select
                            value={selectedYear}
                            onChange={(e) =>
                                setSelectedYear(e.target.value)
                            }
                        >
                            <option value="">All Years</option>

                            {[...new Set(
                                datafromapi.map(car => car.year)
                            )]
                                .sort((a, b) => b - a)
                                .map(year => (
                                    <option
                                        key={year}
                                        value={year}
                                    >
                                        {year}
                                    </option>
                                ))
                            }

                        </select>
                    
                </div>
                     </div>    
                    </div>

                </div>

              
        {/* CARS */}

        <div className="cars-section">

            <h2 className="section-title">
                Cars
                <span className="car-count">
                    {filteredCars.length} cars
                </span>
            </h2>

            <div className="cars-grid">

                {filteredCars.map((car) => (

                    <div
                        key={car.id}
                        className="car-card"
                    >

                        <h3 className="car-title">
                            {car.brand.brand} {car.model}
                        </h3>

                        <p className="car-info">
                            <strong>Colour:</strong>{" "}
                            {car.colour}
                        </p>

                        <p className="car-info">
                            <strong>Year:</strong>{" "}
                            {car.year}
                        </p>

                        <p className="car-price">
                            <strong>Price:</strong>{" "}
                            ₹{car.price}
                        </p>

                        <p className="car-date">
                            <strong>Posted Date:</strong>{" "}
                            {car.created_at.split("T")[0]}
                        </p>

                        <p className="car-info">
                            <strong>
                                <i className="bi bi-fuel-pump-diesel"></i>
                                {" "}Fuel Type:
                            </strong>{" "}
                            {car.fueltype.fueltype}
                        </p>

                        <p className="car-info">
                            <strong>
                                <i className="bi bi-gear"></i>
                                {" "}Gear Type:
                            </strong>{" "}
                            {car.geartype.geartype}
                        </p>

                        <p className="car-price">
                            <strong>Car Location:</strong>{" "}
                            {car.carlocation}
                        </p>

                        <div className="car-actions">

                            <button
                                className="btn btn-book"
                                onClick={() =>
                                    handleCarbookingbtn()
                                }
                            >
                                Book Car
                            </button>

                        </div>

                    </div>

                ))}

            </div>

        </div>
  

                 <div className="chatbot-container">

                    {chatOpen && (
                    <div className="chatbot-window">

                        <div className="chatbot-header">
                            <div>
                                <h3>Car Assistant</h3>
                                <span>● Online</span>
                            </div>

                            <button
                                className="chatbot-close"
                                onClick={() => setChatOpen(false)}
                            >
                                ×
                            </button>
                        </div>

                        <div className="chatbot-messages">

                            <div className="bot-message">
                                👋 Hi! I'm your Car Assistant.
                                <br />
                                How can I help you?
                            </div>

                            <div className="bot-message">
                                You can ask me about cars, prices,
                                models, fuel type, location and more.
                            </div>

                        </div>

                        <div className="chatbot-input">
                            <input
                                type="text"
                                placeholder="Ask about cars..."
                            />

                            <button>
                                <i className="bi bi-send-fill"></i>
                            </button>
                        </div>

                    </div>
                )}

                <button
                    className="chatbot-button"
                    onClick={() => setChatOpen(!chatOpen)}
                >
                    <i className="bi bi-chat-dots-fill"></i>
                </button>

            </div>
                

    </>
               )
                    }

export default Home