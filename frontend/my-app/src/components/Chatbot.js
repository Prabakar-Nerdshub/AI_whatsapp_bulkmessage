import React, { useState } from "react";
import axios from "axios";
import CONFIG from "../config";
import {
  Card, CardContent, CardActions, Button,
  Typography, CircularProgress, Snackbar, Alert, Grid
} from "@mui/material";

const Chatbot = ({ confirmedContacts = [], selectedGroup }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);

  const handleSendMessage = async () => {
    if (!selectedGroup) {
      setError("Please select a file group.");
      return;
    }

    if (!Array.isArray(confirmedContacts) || confirmedContacts.length === 0) {
      setError("No contacts selected.");
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post(`${CONFIG.API_BASE_URL}/send_whatsapp_message`, {
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
      <Grid container spacing={2} sx={{ width: "100%" }}>
        {/* Main Card */}
        <Grid item xs={6}>
          <Card className="shadow-lg rounded-lg" sx={{ width: "100%", padding: "16px", boxShadow: 3 }}>
            <CardContent>
              <Typography variant="h5" gutterBottom>
                Send WhatsApp Message
              </Typography>

              <Typography variant="body1" color="textSecondary" sx={{ mb: 2 }}>
                Selected Group: {selectedGroup ? String(selectedGroup) : "None"}
              </Typography>

              {Array.isArray(confirmedContacts) && confirmedContacts.length > 0 && (
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
                sx={{ width: "50%" }}
                disabled={loading}
              >
                {loading ? <CircularProgress size={24} /> : "Send"}
              </Button>
            </CardActions>
          </Card>
        </Grid>

        {/* Placeholder Card */}
        <Grid item xs={6}>
          <Card className="shadow-lg rounded-lg" sx={{ width: "100%", padding: "16px", boxShadow: 3 }}>
            <CardContent>
              <Typography variant="h5" color="textSecondary">
                Future Content Area
              </Typography>
              <Typography variant="body2" color="textSecondary">
                This space is reserved for future content or functionality.
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Snackbar open={!!error} autoHideDuration={3000} onClose={() => setError("")}>
        <Alert onClose={() => setError("")} severity="error">
          {error}
        </Alert>
      </Snackbar>

      <Snackbar open={success} autoHideDuration={3000} onClose={() => setSuccess(false)}>
        <Alert onClose={() => setSuccess(false)} severity="success">
          Message sent successfully!
        </Alert>
      </Snackbar>
    </div>
  );
};

export default Chatbot;
