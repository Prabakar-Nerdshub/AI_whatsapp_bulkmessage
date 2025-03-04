import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import * as XLSX from "xlsx";
import Papa from "papaparse";
import { Card, CardContent, Typography, Button, Input, Box, Snackbar, Alert, Dialog } from "@mui/material";

const DataConnectorPopup = ({ open, handleClose }) => {
    const [file, setFile] = useState(null);
    const [openSnackbar, setOpenSnackbar] = useState(false);
    const navigate = useNavigate();

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    const extractContacts = async (file) => {
        return new Promise((resolve, reject) => {
            const fileExtension = file.name.split(".").pop().toLowerCase();

            if (fileExtension === "csv") {
                Papa.parse(file, {
                    complete: (result) => {
                        const contacts = result.data.map(row => ({
                            name: row["Name"],
                            phoneNumber: row["Phone Number"],
                            area: row["Area"]
                        })).filter(contact => contact.name && contact.phoneNumber && contact.area);
                        resolve(contacts);
                    },
                    header: true
                });
            } else if (fileExtension === "xlsx" || fileExtension === "xls") {
                const reader = new FileReader();
                reader.onload = (e) => {
                    const data = new Uint8Array(e.target.result);
                    const workbook = XLSX.read(data, { type: "array" });
                    const sheetName = workbook.SheetNames[0];
                    const sheet = workbook.Sheets[sheetName];
                    const jsonData = XLSX.utils.sheet_to_json(sheet);

                    const contacts = jsonData.map(row => ({
                        name: row["Name"],
                        phoneNumber: row["Phone Number"],
                        area: row["Area"]
                    })).filter(contact => contact.name && contact.phoneNumber && contact.area);

                    resolve(contacts);
                };
                reader.readAsArrayBuffer(file);
            } else {
                resolve([]);
            }
        });
    };

    const handleUpload = async () => {
        if (!file) {
            alert("Please select a file first.");
            return;
        }

        try {
            const contacts = await extractContacts(file);
            localStorage.setItem("uploadedContacts", JSON.stringify(contacts));

            setOpenSnackbar(true);
            navigate("/chatbot");
        } catch (error) {
            console.error("Error processing file:", error);
        }
    };

    return (
        <Dialog open={open} onClose={handleClose}>
            <Card sx={{ maxWidth: 400, mx: "auto", mt: 4, p: 2, boxShadow: 3 }}>
                <CardContent>
                    <Typography variant="h6">Upload Contact List</Typography>
                    <Box display="flex" flexDirection="column" gap={2}>
                        <Input type="file" onChange={handleFileChange} />
                        <Button variant="contained" onClick={handleUpload}>Upload</Button>
                    </Box>
                </CardContent>
                <Snackbar open={openSnackbar} autoHideDuration={3000} onClose={() => setOpenSnackbar(false)}>
                    <Alert severity="success">File uploaded successfully!</Alert>
                </Snackbar>
            </Card>
        </Dialog>
    );
};

export default DataConnectorPopup;
