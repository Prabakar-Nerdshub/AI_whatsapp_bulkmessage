import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { CssBaseline, Box } from "@mui/material";
import { ThemeProvider, createTheme } from "@mui/material/styles";
import axios from "axios";

import Sidebar from "./components/Sidebar";
import Login from "./components/Login";
import Chatbot from "./components/Chatbot";
import DataConnectorPopup from "./components/DataConnectorPopup";
import FAQ from "./components/FAQPopup";
import ContactList from "./components/ContactList";
import PrivacyPolicy from "./components/PrivacyPolicy";
import TermsandConditions from "./components/TermsandConditions";

const theme = createTheme({
  palette: {
    primary: { main: "#1976d2" },
    background: { default: "#f5f5f5" },
  },
});

const App = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [confirmedContacts, setConfirmedContacts] = useState([]);
  const [fileGroups, setFileGroups] = useState([]);
  const [selectedGroup, setSelectedGroup] = useState("");

  const fetchFileGroups = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:8000/api/file_groups/");
      setFileGroups(response.data.groups || []);
    } catch (error) {
      console.error("Error fetching file groups:", error);
    }
  };

  useEffect(() => {
    if (isAuthenticated) fetchFileGroups();
  }, [isAuthenticated]);

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Box
          sx={{
            display: "flex",
            height: "100vh",
            backgroundImage: "url('/background2.png')",
            backgroundSize: "100%",
            backgroundPosition: "bottom",
            backgroundRepeat: "no-repeat",
          }}
        >
          {isAuthenticated && <Sidebar />}
          <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
            <Routes>
              <Route path="/" element={<Login setIsAuthenticated={setIsAuthenticated} />} />
              <Route
                path="/chatbot"
                element={
                  isAuthenticated ? (
                    <Chatbot confirmedContacts={confirmedContacts} selectedGroup={selectedGroup} />
                  ) : (
                    <Login setIsAuthenticated={setIsAuthenticated} />
                  )
                }
              />
              <Route
                path="/data-connector"
                element={
                  isAuthenticated ? (
                    <DataConnectorPopup fetchFileGroups={fetchFileGroups} />
                  ) : (
                    <Login setIsAuthenticated={setIsAuthenticated} />
                  )
                }
              />
              <Route path="/faq" element={isAuthenticated ? <FAQ /> : <Login setIsAuthenticated={setIsAuthenticated} />} />
              <Route
                path="/contact-list"
                element={
                  isAuthenticated ? (
                    <ContactList
                      setConfirmedContacts={setConfirmedContacts}
                      fileGroups={fileGroups}
                      selectedGroup={selectedGroup}
                      setSelectedGroup={setSelectedGroup}
                    />
                  ) : (
                    <Login setIsAuthenticated={setIsAuthenticated} />
                  )
                }
              />
              {/* Privacy Policy Route */}
              <Route path="/privacy-policy" element={<PrivacyPolicy />} />

              {/* Terms and Conditions Route */}
              <Route path="/terms-and-conditions" element={<TermsandConditions />} />
            </Routes>
          </Box>
        </Box>
      </Router>
    </ThemeProvider>
  );
};

export default App;
