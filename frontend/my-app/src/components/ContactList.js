import React, { useState, useEffect } from "react";
import axios from "axios";
import {
  Table, TableBody, TableCell, TableContainer,
  TableHead, TableRow, Paper, Checkbox, Button,
  Snackbar, Alert, CircularProgress, Typography,
  FormControl, Select, MenuItem, InputLabel
} from "@mui/material";

const ContactList = ({ setConfirmedContacts, fileGroups, selectedGroup, setSelectedGroup }) => {
  const [contacts, setContacts] = useState([]);
  const [selectedContacts, setSelectedContacts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [openSnackbar, setOpenSnackbar] = useState(false);
  const [selectAll, setSelectAll] = useState(false);

  // Fetch contacts when a new group is selected
  useEffect(() => {
    if (selectedGroup) fetchContacts(selectedGroup);
  }, [selectedGroup]);

  const fetchContacts = async (group) => {
    setLoading(true);
    try {
      const response = await axios.get(`http://127.0.0.1:8000/api/get_contacts/${group}/`);
      setContacts(response.data.contacts || []);
      setSelectedContacts([]); // Reset selection on new fetch
      setSelectAll(false); // Reset "Select All" state
    } catch (error) {
      setError("Failed to fetch contacts.");
    } finally {
      setLoading(false);
    }
  };

  // Toggle selection of individual contacts
  const handleContactSelect = (contact) => {
    setSelectedContacts((prev) =>
      prev.includes(contact)
        ? prev.filter((c) => c !== contact)
        : [...prev, contact]
    );
  };

  // Handle "Select All" checkbox
  const handleSelectAll = () => {
    if (selectAll) {
      setSelectedContacts([]);
    } else {
      setSelectedContacts(contacts);
    }
    setSelectAll(!selectAll);
  };

  const handleConfirmSelection = () => {
    setConfirmedContacts(selectedContacts);
    setOpenSnackbar(true);
  };

  return (
    <div>
      {/* Dropdown to select contact group */}
      <FormControl fullWidth sx={{ mb: 2 }}>
        <InputLabel>Select Contact Group</InputLabel>
        <Select value={selectedGroup} onChange={(e) => setSelectedGroup(e.target.value)}>
          {fileGroups.map((group, index) => (
            <MenuItem key={index} value={group.name}>{group.name}</MenuItem>
          ))}
        </Select>
      </FormControl>

      {/* Confirm Selection Button */}
      <Button variant="contained" color="primary" onClick={handleConfirmSelection} sx={{ mb: 2 }}>
        Confirm Selection
      </Button>

      {/* Display contacts below the button */}
      {loading ? (
        <CircularProgress />
      ) : contacts.length > 0 ? (
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>
                  <Checkbox
                    checked={selectAll}
                    indeterminate={selectedContacts.length > 0 && selectedContacts.length < contacts.length}
                    onChange={handleSelectAll}
                  />
                  Select All
                </TableCell>
                <TableCell>Name</TableCell>
                <TableCell>Phone Number</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {contacts.map((contact, index) => (
                <TableRow key={index}>
                  <TableCell>
                    <Checkbox
                      checked={selectedContacts.includes(contact)}
                      onChange={() => handleContactSelect(contact)}
                    />
                  </TableCell>
                  <TableCell>{contact.name}</TableCell>
                  <TableCell>{contact.phone_numbers}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      ) : (
        <Typography variant="body1" color="textSecondary" sx={{ mt: 2 }}>
          No contacts available.
        </Typography>
      )}

      {/* Snackbar notification */}
      <Snackbar open={openSnackbar} autoHideDuration={3000} onClose={() => setOpenSnackbar(false)}>
        <Alert onClose={() => setOpenSnackbar(false)} severity="success">
          Contacts confirmed!
        </Alert>
      </Snackbar>
    </div>
  );
};

export default ContactList;
