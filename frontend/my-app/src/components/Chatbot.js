import React, { useState } from "react";
import axios from "axios";
import {
  Card, CardContent, CardActions, Button,
  Typography, CircularProgress, Snackbar, Alert
} from "@mui/material";

const Chatbot = ({ confirmedContacts, selectedGroup }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);

  const handleSendMessage = async () => {
    if (!selectedGroup) {
      setError("Please select a file group.");
      return;
    }

    if (confirmedContacts.length === 0) {
      setError("No contacts selected.");
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post("http://127.0.0.1:8000/api/send_whatsapp_message", {
        group_name: selectedGroup,
        contacts: confirmedContacts,
      });

      if (response.status === 200) {
        setSuccess(true);
      } else {
        setError("Failed to send messages.");
      }
    } catch (error) {
      console.error("Error sending messages:", error);
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

          <Typography variant="body1" color="textSecondary" sx={{ mb: 2 }}>
            Selected Group: {selectedGroup || "None"}
          </Typography>

          {confirmedContacts.length > 0 && (
            <Typography variant="body1" color="textSecondary" sx={{ mt: 2 }}>
              Selected Contacts: {confirmedContacts.length}
            </Typography>
          )}
        </CardContent>

        <CardActions>
          <Button
            onClick={handleSendMessage}
            variant="contained"
            color="primary"
            size="small"
            fullWidth
            disabled={loading}
          >
            {loading ? <CircularProgress size={20} /> : "Send"}
          </Button>
        </CardActions>
      </Card>

      <Snackbar
        open={success}
        autoHideDuration={3000}
        onClose={() => setSuccess(false)}
      >
        <Alert onClose={() => setSuccess(false)} severity="success">
          Message sent successfully!
        </Alert>
      </Snackbar>
    </div>
  );
};

export default Chatbot;
