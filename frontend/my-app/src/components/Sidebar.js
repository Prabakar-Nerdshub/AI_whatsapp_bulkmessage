import React, { useState } from "react";
import {
  Drawer,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Dialog,
  Box,
} from "@mui/material";
import {
  MobileScreenShare as ChatIcon,
  CloudUpload as UploadIcon,
  Contacts as ContactsIcon,
  Analytics as AnalyticsIcon,
  HelpOutline as FAQIcon,
  Policy as PrivacyIcon,
  Gavel as TermsIcon,
} from "@mui/icons-material";
import logo from "../assets/nerdslogo1.png";
import { useNavigate } from "react-router-dom";
import DataConnectorPopup from "./DataConnectorPopup";
import FAQPopup from "./FAQPopup";

const Sidebar = () => {
  const navigate = useNavigate();
  const [openDataConnector, setOpenDataConnector] = useState(false);
  const [openFAQ, setOpenFAQ] = useState(false);

  return (
    <Drawer
      variant="permanent"
      sx={{
        width: 240,
        flexShrink: 0,
        "& .MuiDrawer-paper": {
          width: 240,
          boxSizing: "border-box",
        },
      }}
    >
      {/* Logo Section */}
      <Box
        sx={{
          width: "100%",
          padding: 2,
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          borderBottom: "1px solid #ccc",
        }}
      >
        <img
          src={logo}
          style={{
            width: "100%",
            maxWidth: "300px",
            height: "auto",
            objectFit: "contain",
          }}
        />
      </Box>

      {/* Navigation Links */}
      <List sx={{ width: 240, padding: 2 }}>
        <ListItem button onClick={() => navigate("/chatbot")}>
          <ListItemIcon><ChatIcon /></ListItemIcon>
          <ListItemText primary="Message Broadcast" />
        </ListItem>

        <ListItem button onClick={() => setOpenDataConnector(true)}>
          <ListItemIcon><UploadIcon /></ListItemIcon>
          <ListItemText primary="Upload Contact List" />
        </ListItem>

        <ListItem button onClick={() => navigate("/contact-list")}>
          <ListItemIcon><ContactsIcon /></ListItemIcon>
          <ListItemText primary="Customers" />
        </ListItem>

        <ListItem button onClick={() => navigate("/analytics")}>
          <ListItemIcon><AnalyticsIcon /></ListItemIcon>
          <ListItemText primary="Analytics" />
        </ListItem>

        <ListItem button onClick={() => setOpenFAQ(true)}>
          <ListItemIcon><FAQIcon /></ListItemIcon>
          <ListItemText primary="FAQ" />
        </ListItem>

        <ListItem button onClick={() => navigate("/privacy-policy")}>
          <ListItemIcon><PrivacyIcon /></ListItemIcon>
          <ListItemText primary="Privacy Policy" />
        </ListItem>

        <ListItem button onClick={() => navigate("/Terms-and-Conditions")}>
          <ListItemIcon><TermsIcon /></ListItemIcon>
          <ListItemText primary="Terms and Conditions" />
        </ListItem>
      </List>

      {/* Data Connector Popup */}
      <Dialog open={openDataConnector} onClose={() => setOpenDataConnector(false)}>
        <DataConnectorPopup
          open={openDataConnector}
          handleClose={() => setOpenDataConnector(false)}
        />
      </Dialog>

      {/* FAQ Popup */}
      <Dialog open={openFAQ} onClose={() => setOpenFAQ(false)}>
        <FAQPopup open={openFAQ} handleClose={() => setOpenFAQ(false)} />
      </Dialog>
    </Drawer>
  );
};

export default Sidebar;
