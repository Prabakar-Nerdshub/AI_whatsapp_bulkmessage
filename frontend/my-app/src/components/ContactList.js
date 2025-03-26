import React, { useState, useEffect } from "react";
import axios from "axios";
import CONFIG from "../config";
import {
  Table, TableBody, TableCell, TableContainer,
  TableHead, TableRow, Paper, Checkbox, Button,
  Snackbar, Alert, CircularProgress, Typography,
  FormControl, Select, MenuItem, InputLabel
} from "@mui/material";

const ContactList = ({ setConfirmedContacts, fileGroups = [], selectedGroup, setSelectedGroup }) => {
  const [contacts, setContacts] = useState([]);
  const [selectedContacts, setSelectedContacts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [openSnackbar, setOpenSnackbar] = useState(false);
  const [selectAll, setSelectAll] = useState(false);

  useEffect(() => {
    if (selectedGroup) fetchContacts(selectedGroup);
  }, [selectedGroup]);

  const fetchContacts = async (group) => {
    setLoading(true);
    try {
      const response = await axios.get(`${CONFIG.API_BASE_URL}/api/get_contacts/${group}/`);
      setContacts(Array.isArray(response.data.contacts) ? response.data.contacts : []);
      setSelectedContacts([]); // Reset selection on new fetch
      setSelectAll(false);
    } catch (error) {
      console.error("Error fetching contacts:", error);
      setError("Failed to fetch contacts.");
    } finally {
      setLoading(false);
    }
  };

  const handleContactSelect = (contact) => {
    setSelectedContacts((prev) =>
      prev.includes(contact) ? prev.filter((c) => c !== contact) : [...prev, contact]
    );
  };

  const handleSelectAll = () => {
    setSelectedContacts(selectAll ? [] : [...contacts]);
    setSelectAll(!selectAll);
  };

  const handleConfirmSelection = () => {
    setConfirmedContacts([...selectedContacts]);
    setOpenSnackbar(true);
  };

  return (
    <div>
      <FormControl fullWidth sx={{ mb: 2 }}>
        <InputLabel>Select Contact Group</InputLabel>
        <Select value={selectedGroup || ""} onChange={(e) => setSelectedGroup(e.target.value)}>
          {fileGroups.map((group, index) => (
            <MenuItem key={index} value={group.name}>{String(group.name)}</MenuItem>
          ))}
        </Select>
      </FormControl>

      <Button variant="contained" color="primary" onClick={handleConfirmSelection} sx={{ mb: 2 }}>
        Confirm Selection
      </Button>

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
                  <TableCell>{String(contact.name)}</TableCell>
                  <TableCell>{String(contact.phone_numbers)}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      ) : (
        <Typography>No contacts available.</Typography>
      )}
    </div>
  );
};

export default ContactList;
