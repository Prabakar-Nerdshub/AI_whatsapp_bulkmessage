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
  Select,
} from "@mui/material";
import nerdsLogo from "../assets/nerdslogo.png"; // ✅ Replace with your actual path

const Chatbot = ({ confirmedContacts = [], selectedGroup }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);
  const [selectedTemplate, setSelectedTemplate] = useState("");
  const [insights, setInsights] = useState(null);

  const templates = [
    {
      name: "nerdshub_sara",
      language: "Malay",
      status: "Active – Quality",
      messagePreview: "Hi Saya sebuah ChatBot Automasi ..."
    },
    {
      name: "sara_list_message",
      language: "Malay",
      status: "Active – Quality",
      messagePreview: "Hi Saya sebuah ChatBot Automasi ..."
    },
    {
      name: "sara_interactive_custom",
      language: "English",
      status: "Active – Quality",
      messagePreview: "Hi Saya sebuah ChatBot Automasi ..."
    },
    {
      name: "custom_temp1",
      language: "English",
      status: "Active – Quality",
      messagePreview: "Hi Saya sebuah ChatBot Automasi ..."
    },
    {
      name: "blackfriday",
      language: "English",
      status: "Active – Quality",
      messagePreview: "Black Friday is around the corner and as promised we are given you early access to our deals. Select the best deal for the product you are intrested in!"
    }
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
        fetchInsights();
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
    <div className="flex justify-center items-center bg-gray-100 p-4">
      <Grid container spacing={2}>
        {/* Left side */}
        <Grid item xs={12} md={6}>
          <Card sx={{ padding: 2, boxShadow: 3 }}>
            <CardContent>
              <Typography variant="h5" gutterBottom>
                Send WhatsApp Message
              </Typography>

              <Typography variant="body1" color="textSecondary">
                Selected Customer: {selectedGroup || "None"}
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

          {/* Chat Preview */}
          <Card
            sx={{
              width: "80%",
              mt: 2,
              padding: 2,
              backgroundColor: "#e5ddd5",
              borderRadius: "12px",
              boxShadow: 3,
              maxHeight: 500,
              overflowY: "auto",
            }}
          >
            {/* Header */}
            <div style={{ display: "flex", alignItems: "center", marginBottom: 16 }}>
              <img
                src="/nerdslogo.png"
                alt="nerdshub logo"
                style={{ width: 40, height: 40, borderRadius: "50%", marginRight: 12 }}
              />
              <div>
                <Typography variant="subtitle1" fontWeight="bold">
                  Nerdshub
                </Typography>
                <Typography variant="caption" color="textSecondary">
                  Business Account
                </Typography>
              </div>
            </div>

            {/* Message bubbles */}
            <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
              {/* Bot Message 1 */}
              <div
                style={{
                  alignSelf: "flex-start",
                  background: "#fff",
                  borderRadius: "12px",
                  padding: "10px 14px",
                  fontSize: "13px",
                  lineHeight: "1.5",
                  maxWidth: "100%",
                }}
              >
                <strong>Salam MyKasih!</strong><br />
                Hi<br />
                Saya sebuah ChatBot Automasi (bukan manusia). I am an <br />
                Automated ChatBot (non-human) Bagaimana boleh saya bantu anda?<br />
                    
                How can I help you?
                Sila pilih
                
                <div
                style={{
                  alignSelf: "flex-end",
                  background: "#dcf8c6",
                  borderRadius: "12px",
                  padding: "10px 14px",
                  maxWidth: "41%",
                }}
              >
                <div
                  style={{
                    backgroundColor: "#25D366",
                    color: "white",
                    borderRadius: "6px",
                    padding: "6px 10px",
                    display: "inline-block",
                    fontWeight: "bold",
                    fontSize: "13px",
                  }}
                >
                  📄 Senarai Pilihan
                </div>
              </div>
              <Typography variant="caption" color="textSecondary" sx={{ float: "right", fontSize: "10px", mt: 1 }}>
                  5:08 pm
                </Typography>
              </div>

              {/* User Response Bubble */}
              <div
                style={{
                  alignSelf: "flex-end",
                  background: "#dcf8c6",
                  borderRadius: "12px",
                  padding: "10px 14px",
                  maxWidth: "60%",
                }}
                >
                <div>
                  <Typography variant="body2">Selected Option : Program SARA 2025</Typography>
                </div>
                <Typography variant="caption" color="textSecondary" sx={{ float: "right", fontSize: "10px", mt: 1 }}>
                  5:08 pm
                </Typography>
              </div>

              {/* Bot Message 2 */}
              <div
                style={{
                  alignSelf: "flex-start",
                  background: "#fff",
                  borderRadius: "12px",
                  padding: "10px 14px",
                  fontSize: "13px",
                  lineHeight: "1.5",
                  maxWidth: "80%",
                }}
              >
                <Typography variant="body2">
                  Sumbangan Asas Rahmah (SARA) merupakan program bantuan bersasar kepada rakyat yang paling terkesan dengan gelumang kos sara hidup. <br /><br />
                  Program ini untuk mengangkat taraf ekonomi golongan rentan dan menjunjung prinsip kesaksamaan yang menjadi teras kepada kerangka Ekonomi MADANI. <br /><br />
                  Penerima STR 2025 yang telah disahkan daripada data Miskin Tegar dan Miskin eKasih layak SARA 2025 berjumlah RM100 / RM50 setiap bulan bagi tempoh 12 bulan (Januari 2025 - Disember 2025). <br /><br />
                  Manakala kadar tambahan kepada semua penerima STR 2025 kategori Isi Rumah dan Warga Emas Tiada Pasangan adalah RM100 / RM50 setiap bulan bagi tempoh 9 bulan (April 2025 - Disember 2025).
                </Typography>
                <Typography variant="caption" color="textSecondary" sx={{ float: "right", fontSize: "10px", mt: 1 }}>
                  5:08 pm
                </Typography>
              </div>
            </div>
          </Card>
        </Grid>

        {/* Right side */}
        <Grid item xs={12} md={6}>
          <Card sx={{ padding: 2, boxShadow: 3 }}>
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

      {/* Snackbar */}
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
