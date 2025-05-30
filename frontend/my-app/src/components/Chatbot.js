import React, { useState, useEffect } from "react";
import axios from "axios";
import CONFIG from "../config";
import {
  Card,
  CardContent,
  CardActions,
  Button,
  Typography,
  CircularProgress,
  Snackbar,
  Alert,
  Grid,
  MenuItem,
  FormControl,
  InputLabel,
  Select
} from "@mui/material";

const Chatbot = ({ confirmedContacts = [], selectedGroup }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);
  const [selectedTemplate, setSelectedTemplate] = useState("");
  const [insights, setInsights] = useState(null);

  // Static template list (can be fetched dynamically)
  const templates = [
    {
      name: "nerdshub_sara",
      language: "Malay",
      status: "Active – Quality",
      messagePreview: "Hi Saya sebuah ChatBot Automasi ..."
    },
    // Add more templates here if needed
  ];

  const handleSendMessage = async () => {
    if (!selectedGroup) {
      setError("Please select a file group.");
      return;
    }

    if (!Array.isArray(confirmedContacts) || confirmedContacts.length === 0) {
      setError("No contacts selected.");
      return;
    }

    if (!selectedTemplate) {
      setError("Please select a message template.");
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post(`${CONFIG.API_BASE_URL}/api/send_whatsapp_message`, {
        group_name: selectedGroup,
        contacts: confirmedContacts,
        template_name: selectedTemplate,
      });

      if (response.status === 200) {
        setSuccess(true);
        fetchInsights(); // refresh insights after sending
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

  const fetchInsights = async () => {
    try {
      const response = await axios.get(`${CONFIG.API_BASE_URL}/api/fetch_whatsapp_insights/`);
      setInsights(response.data);
    } catch (err) {
      console.error("Failed to fetch WhatsApp insights:", err);
    }
  };

  useEffect(() => {
    fetchInsights();
  }, []);

  return (
    <div className="flex justify-center items-center h-screen bg-gray-100">
      <Grid container spacing={2} sx={{ width: "100%" }}>
        {/* Left Card - Message Send Info */}
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

             {/* {insights && (
                <div style={{ marginTop: "20px" }}>
                  <Typography variant="subtitle1" gutterBottom>WhatsApp Insights</Typography>
                  <Typography variant="body2">Messages Sent: {insights.messages_sent}</Typography>
                  <Typography variant="body2">Messages Delivered: {insights.messages_delivered}</Typography>
                  <Typography variant="body2">Messages Read: {insights.messages_read}</Typography>
                </div>
              )}*/}
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

        {/* Right Card - Template Selector */}
        <Grid item xs={6}>
          <Card className="shadow-lg rounded-lg" sx={{ width: "100%", padding: "16px", boxShadow: 3 }}>
            <CardContent>
              <Typography variant="h5" gutterBottom>
                Select Template
              </Typography>

              <FormControl fullWidth sx={{ mt: 2 }}>
                <InputLabel id="template-select-label">Template</InputLabel>
                <Select
                  labelId="template-select-label"
                  value={selectedTemplate}
                  label="Template"
                  onChange={(e) => setSelectedTemplate(e.target.value)}
                >
                  {templates.map((template) => (
                    <MenuItem key={template.name} value={template.name}>
                      {template.name} ({template.language})
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>

              {selectedTemplate && (
                <>
                  <Typography variant="body2" color="textSecondary" sx={{ mt: 2 }}>
                    Status: {templates.find(t => t.name === selectedTemplate)?.status}
                  </Typography>
                  <Typography variant="body2" color="textSecondary" sx={{ mt: 1 }}>
                    Message Preview: {templates.find(t => t.name === selectedTemplate)?.messagePreview}
                  </Typography>
                </>
              )}
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Error Snackbar */}
      <Snackbar open={!!error} autoHideDuration={3000} onClose={() => setError("")}>
        <Alert onClose={() => setError("")} severity="error">
          {error}
        </Alert>
      </Snackbar>

      {/* Success Snackbar */}
      <Snackbar open={success} autoHideDuration={3000} onClose={() => setSuccess(false)}>
        <Alert onClose={() => setSuccess(false)} severity="success">
          Message sent successfully!
        </Alert>
      </Snackbar>
    </div>
  );
};

export default Chatbot;
