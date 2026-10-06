import { ArrowRight } from 'react-bootstrap-icons';
import { useState } from "react";
import chatboticon from  '../assets/chatboticon.webp'; 
import '../sytles/chatbot.css'
function Chatbot(){

    const [chatOpen,setChatbotOpen] = useState(false)
    const [inputchatbot, setchatbotinput] = useState("");
    
    const [chatMessages, setChatMessages] = useState([
    {
        sender: "bot",
        message: "👋 Hi! I'm your Car Assistant."
    },
    {
        sender: "bot",
        message: "You can ask me about cars, prices, models, fuel type, location and more."
    }
]);

const [chatLoading, setChatLoading] = useState(false);
    const submitquerrytochatbor = async (e) => {
    e.preventDefault();

    const query = inputchatbot.trim();

    // Don't send empty messages
    if (!query) {
        return;
    }

    // Immediately add user's message
    setChatMessages((previousMessages) => [
        ...previousMessages,
        {
            sender: "user",
            message: query
        }
    ]);

    // Clear input
    setchatbotinput("");

    setChatLoading(true);

    try {

        const formdata = {
            query: query
        };

        const res = await api.post("/api/rag/", formdata);

        // console.log("RAG RESPONSE:", res.data);

        // Add bot response
        setChatMessages((previousMessages) => [
            ...previousMessages,
            {
                sender: "bot",
                message: res.data.answer
            }
        ]);

    } catch (error) {

        console.log("RAG ERROR:", error.response?.data);

        setChatMessages((previousMessages) => [
            ...previousMessages,
            {
                sender: "bot",
                message:
                    error.response?.data?.detail ||
                    "Sorry, something went wrong. Please try again."
            }
        ]);

    } finally {
        setChatLoading(false);
    }
};
    return(
         <div className="chatbot-container">

    {chatOpen && (
        <div className="chatbot-window">

            {/* HEADER */}

            <div className="chatbot-header">

                <div>
                    <h3>Car Assistant</h3>
                    <span>●</span>
                    <span> Online</span>
                </div>

                <button
                    className="chatbot-close"
                    onClick={() => setChatbotOpen(false)}
                >
                    ×
                </button>

            </div>


            {/* MESSAGES */}

            <div className="chatbot-messages">

                {chatMessages.map((chat, index) => (

                    <div
                        key={index}
                        className={
                            chat.sender === "user"
                                ? "user-message"
                                : "bot-message"
                        }
                    >
                        {chat.message}
                    </div>

                ))}

                {chatLoading && (
                    <div className="bot-message typing-message">
                        Thinking...
                    </div>
                )}

            </div>


            {/* INPUT */}

            <div className="chatbot-input">

                <form
                    className="input-submit"
                    onSubmit={submitquerrytochatbor}
                >
                    <div class="input-group">
                        <input
                            type="text"
                            placeholder="Ask about cars..."
                            value={inputchatbot}
                            onChange={(e) =>
                                setchatbotinput(e.target.value)
                            }
                            disabled={chatLoading}
                        />
                        <div>
                            <button
                            type="submit"
                            disabled={
                                chatLoading ||
                                !inputchatbot.trim()
                            }
                        >
                            <ArrowRight size={20} />
                        </button>
                        </div>
                        
                            
                    </div>
                </form>

            </div>

        </div>
    )}


    {/* FLOATING BUTTON */}

    <button
        className="chatbot-button"
        onClick={() => setChatbotOpen(!chatOpen)}
    >
        <img className="chatboticon" src={chatboticon} alt="" />
    </button>

</div>
       
    )
}
export default Chatbot