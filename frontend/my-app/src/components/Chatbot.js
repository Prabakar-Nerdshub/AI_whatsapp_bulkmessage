import React, { useState } from "react";
import axios from "axios";
import {
  Card,
  CardContent,
  CardActions,
  TextField,
  Button,
  Typography,
  CircularProgress,
  Select,
  MenuItem,
  InputLabel,
  FormControl,
} from "@mui/material";

const Chatbot = () => {
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [countryCode, setCountryCode] = useState("+91"); // Default to India

  const handleSendMessage = async () => {
    if (!message.trim()) {
      alert("Please enter a message.");
      return;
    }

    // Retrieve stored phone numbers from localStorage
    const phoneNumbers = JSON.parse(localStorage.getItem("uploadedPhoneNumbers")) || [];

    console.log("Retrieved Phone Numbers:", phoneNumbers); // Debugging log

    if (phoneNumbers.length === 0) {
      alert("No phone numbers found in storage.");
      return;
    }

    setLoading(true);

    try {
      const response = await axios.post("http://127.0.0.1:8000/api/send-bulk-messages/", {
        message,
        phoneNumbers,
        countryCode, // Send selected country code
      });

      console.log("Server Response:", response.data);
      alert("Message sent successfully!");
      setMessage(""); // Clear input after sending
    } catch (error) {
      console.error("Error sending message:", error.response?.data);
      alert("Error sending message: " + (error.response?.data?.error || "Unknown error"));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex justify-center items-center h-screen bg-gray-100">
      <Card className="shadow-lg rounded-lg w-96 p-4">
        <CardContent>
          <Typography variant="h5" component="h1" gutterBottom>
            Send a Message
          </Typography>


          {/* Message Input */}
          <TextField
            fullWidth
            multiline
            rows={4}
            variant="outlined"
            label="Enter your message..."
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            disabled={loading}
          />
        </CardContent>

        <CardActions className="p-4">
          <Button
            onClick={handleSendMessage}
            variant="contained"
            color="primary"
            fullWidth
            disabled={loading}
          >
            {loading ? <CircularProgress size={24} /> : "Send"}
          </Button>
        </CardActions>
      </Card>
    </div>
  );
};

export default Chatbot;
