import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { CssBaseline, Box } from "@mui/material";
import { ThemeProvider, createTheme } from "@mui/material/styles";

import Sidebar from "./components/Sidebar";
import Login from "./components/Login";
import Chatbot from "./components/Chatbot";
import DataConnectorPopup from "./components/DataConnectorPopup";
import FAQ from "./components/FAQPopup";

const theme = createTheme({
  palette: {
    primary: { main: "#1976d2" },
    background: { default: "#f5f5f5" },
  },
});

const App = () => {
  const [phoneNumbers, setPhoneNumbers] = useState([]);

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box
        sx={{
          display: "flex",
          height: "100vh",
          backgroundImage: "url('/background.jpg')",
          backgroundSize: "cover",
          backgroundPosition: "center",
          backgroundRepeat: "no-repeat",
        }}
      >
        <Router>
          <Sidebar />
          <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
            <Routes>
              <Route path="/" element={<Login />} />
              <Route path="/chatbot" element={<Chatbot phoneNumbers={phoneNumbers} />} />
              <Route path="/data-connector" element={<DataConnectorPopup setPhoneNumbers={setPhoneNumbers} />} />
              <Route path="/faq" element={<FAQ />} />
            </Routes>
          </Box>
        </Router>
      </Box>
    </ThemeProvider>
  );
};

export default App;
