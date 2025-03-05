import React, { useState } from "react";
import { Drawer, List, ListItem, ListItemText, Select, MenuItem, FormControl, InputLabel, Dialog,} from "@mui/material";
import { useNavigate } from "react-router-dom";
import DataConnectorPopup from "./DataConnectorPopup";
import FAQPopup from "./FAQPopup";

const Sidebar = () => {
  const navigate = useNavigate();
  const [selectedModel, setSelectedModel] = useState("Ollama");
  const [openDataConnector, setOpenDataConnector] = useState(false);
  const [openFAQ, setOpenFAQ] = useState(false);

  return (
    <Drawer variant="permanent" sx={{ width: 240, flexShrink: 0 }}>
      <List sx={{ width: 240, padding: 2 }}>
        {/* Navigation Links */}
        <ListItem button onClick={() => navigate("/chatbot")}>
          <ListItemText primary="Chat Page" />
        </ListItem>

        {/* Model Selection Dropdown with Reduced Size
        <FormControl sx={{ width: "80%", marginBottom: 1 }}>
          <InputLabel>Select Model</InputLabel>
          <Select
            value={selectedModel}
            onChange={(e) => setSelectedModel(e.target.value)}
            sx={{ fontSize: 14, height: 36 }}
          >
            <MenuItem value="Ollama">Ollama</MenuItem>
            <MenuItem value="GPT-4">GPT-4</MenuItem>
          </Select>
        </FormControl>*/}

        {/* Open Data Connector Popup */}
        <ListItem button onClick={() => setOpenDataConnector(true)}>
          <ListItemText primary="Upload Contact List" />
        </ListItem>

        {/* Open FAQ Popup */}
        <ListItem button onClick={() => setOpenFAQ(true)}>
          <ListItemText primary="FAQ" />
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
