import React, { useState } from "react";
import { Drawer, List, ListItem, ListItemText, Dialog } from "@mui/material";
import { useNavigate } from "react-router-dom";
import DataConnectorPopup from "./DataConnectorPopup";
import FAQPopup from "./FAQPopup";

const Sidebar = () => {
  const navigate = useNavigate();
  const [openDataConnector, setOpenDataConnector] = useState(false);
  const [openFAQ, setOpenFAQ] = useState(false);

  return (
    <Drawer variant="permanent" sx={{ width: 240, flexShrink: 0 }}>
      <List sx={{ width: 240, padding: 2 }}>
        {/* Navigation Links */}
        <ListItem button onClick={() => navigate("/chatbot")}>
          <ListItemText primary="Chat Page" />
        </ListItem>

        {/* Open Data Connector Popup */}
        <ListItem button onClick={() => setOpenDataConnector(true)}>
          <ListItemText primary="Upload Contact List" />
        </ListItem>

        <ListItem button onClick={() => navigate("/contact-list")}>
          <ListItemText primary="Contact List" />
        </ListItem>

        {/* Open FAQ Popup */}
        <ListItem button onClick={() => setOpenFAQ(true)}>
          <ListItemText primary="FAQ" />
        </ListItem>

        {/* Navigate to Privacy Policy Page */}
        <ListItem button onClick={() => navigate("/privacy-policy")}>
          <ListItemText primary="Privacy Policy" />
        </ListItem>

        {/* Navigate to Privacy Policy Page */}
        <ListItem button onClick={() => navigate("/Terms-and-Conditions")}>
          <ListItemText primary="Terms and Conditions" />
        </ListItem>

      </List>

      {/* Data Connector Popup */}
      <Dialog open={openDataConnector} onClose={() => setOpenDataConnector(false)}>
        <DataConnectorPopup open={openDataConnector} handleClose={() => setOpenDataConnector(false)} />
      </Dialog>

      {/* FAQ Popup */}
      <Dialog open={openFAQ} onClose={() => setOpenFAQ(false)}>
        <FAQPopup open={openFAQ} handleClose={() => setOpenFAQ(false)} />
      </Dialog>
    </Drawer>
  );
};

export default Sidebar;
