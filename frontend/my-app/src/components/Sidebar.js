import React, { useState } from "react";
import { Drawer, List, ListItem, ListItemText, Dialog, Button, Box, Stack } from "@mui/material";
import { useNavigate } from "react-router-dom";
import DataConnectorPopup from "./DataConnectorPopup";
import FAQPopup from "./FAQPopup";
import ContactList from "./ContactList";
import GroupedContacts from "./GroupedContacts";

const Sidebar = () => {
  const navigate = useNavigate();
  const [openDataConnector, setOpenDataConnector] = useState(false);
  const [openContactList, setOpenContactList] = useState(false);
  const [openFAQ, setOpenFAQ] = useState(false);
  const [openContactReport, setOpenContactReport] = useState(false);
  const [openGroupedContacts, setOpenGroupedContacts] = useState(false);

  return (
    <Drawer variant="permanent" sx={{ width: 240, flexShrink: 0 }}>
      <List sx={{ width: 240, padding: 2 }}>
        <ListItem button onClick={() => navigate("/chatbot")}>
          <ListItemText primary="Chat Page" />
        </ListItem>

        <ListItem button onClick={() => setOpenDataConnector(true)}>
          <ListItemText primary="Upload Contact List" />
        </ListItem>

        <ListItem button onClick={() => setOpenContactReport(true)}>
          <ListItemText primary="Contact Report" />
        </ListItem>

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

      {/* Contact Report Popup */}
      <Dialog open={openContactReport} onClose={() => setOpenContactReport(false)}>
        <Box sx={{ p: 3, minWidth: 800 }}>
          <Stack direction="row" spacing={2}>
            <Button variant="contained" onClick={() => setOpenContactList(true)}>
              Overall Contact List
            </Button>

            <Button variant="contained" onClick={() => setOpenGroupedContacts(true)}>
              Groups
            </Button>
          </Stack>
        </Box>
      </Dialog>

      {/* Contact List Popup */}
      <Dialog open={openContactList} onClose={() => setOpenContactList(false)}>
        <ContactList />
      </Dialog>

      {/* Grouped Contacts Popup */}
      <Dialog open={openGroupedContacts} onClose={() => setOpenGroupedContacts(false)}>
        <GroupedContacts />
      </Dialog>
    </Drawer>
  );
};

export default Sidebar;
