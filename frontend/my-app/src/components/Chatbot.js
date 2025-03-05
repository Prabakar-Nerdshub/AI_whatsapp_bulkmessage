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
  Snackbar,
  Alert,
} from "@mui/material";

const Chatbot = ({ fileId }) => {
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const handleSendMessage = async () => {
  const fileId = localStorage.getItem("uploadedFileId");
    if (!message.trim()) {
      setError("Please enter a message.");
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post("http://127.0.0.1:8000/api/send_whatsapp_message", {
        file_id: fileId,
        message,
      });

      if (response.status === 200) {
        setSuccess("Messages sent successfully.");
        setMessage("");
      } else {
        setError("Failed to send messages.");
      }
    } catch (error) {
      setError("Error sending messages.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex justify-center items-center h-screen bg-gray-100">
      <Card className="shadow-lg rounded-lg w-96 p-4">
        <CardContent>
          <Typography variant="h5" gutterBottom>
            Send WhatsApp Message
          </Typography>
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
        <CardActions>
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

      {/* Error Snackbar */}
      <Snackbar open={!!error} autoHideDuration={4000} onClose={() => setError("")}>
        <Alert severity="error">{error}</Alert>
      </Snackbar>

      {/* Success Snackbar */}
      <Snackbar open={!!success} autoHideDuration={4000} onClose={() => setSuccess("")}>
        <Alert severity="success">{success}</Alert>
      </Snackbar>
    </div>
  );
};

export default Chatbot;
