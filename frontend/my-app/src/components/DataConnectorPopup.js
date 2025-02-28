import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import * as XLSX from "xlsx";
import Papa from "papaparse";
import { Card, CardContent, Typography, Button, Input, Box, Snackbar, Alert, Dialog } from "@mui/material";

const DataConnectorPopup = ({ open, handleClose }) => {
    const [file, setFile] = useState(null);
    const [openSnackbar, setOpenSnackbar] = useState(false);
    const navigate = useNavigate();

    // Handle file selection
    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    // Extract phone numbers from CSV or Excel file
    const extractPhoneNumbers = async (file) => {
        return new Promise((resolve, reject) => {
            const fileExtension = file.name.split(".").pop().toLowerCase();

            if (fileExtension === "csv") {
                Papa.parse(file, {
                    complete: (result) => {
                        console.log("Parsed CSV Headers:", Object.keys(result.data[0] || {})); // Debug
                        const phoneNumbers = result.data
                            .map(row => row["phone numbers"] || row["Phone"] || row["phone"] || row["Phone Number"])
                            .filter(Boolean);
                        resolve(phoneNumbers);
                    },
                    header: true
                });
            } else if (fileExtension === "xlsx" || fileExtension === "xls") {
                const reader = new FileReader();
                reader.onload = (e) => {
                    try {
                        const data = new Uint8Array(e.target.result);
                        const workbook = XLSX.read(data, { type: "array" });
                        const sheetName = workbook.SheetNames[0];
                        const sheet = workbook.Sheets[sheetName];
                        const jsonData = XLSX.utils.sheet_to_json(sheet);
                        console.log("Parsed Excel Headers:", Object.keys(jsonData[0] || {})); // Debug
                        const phoneNumbers = jsonData
                            .map(row => row["phone numbers"] || row["Phone"] || row["phone"] || row["Phone Number"])
                            .filter(Boolean);
                        resolve(phoneNumbers);
                    } catch (error) {
                        reject(error);
                    }
                };
                reader.readAsArrayBuffer(file);
            } else {
                resolve([]);
            }
        });
    };

    // Handle file upload
    const handleUpload = async () => {
        if (!file) {
            alert("Please select a file first.");
            return;
        }

        try {
            const phoneNumbers = await extractPhoneNumbers(file);
            console.log("Extracted Phone Numbers:", phoneNumbers);

            // Store in local storage
            localStorage.setItem("uploadedPhoneNumbers", JSON.stringify(phoneNumbers));

            setOpenSnackbar(true);
            navigate("/chatbot"); // Redirect after upload
        } catch (error) {
            console.error("Error processing file:", error);
        }
    };

    return (
        <Dialog open={open} onClose={handleClose}>
            <Card sx={{ maxWidth: 400, mx: "auto", mt: 4, p: 2, boxShadow: 3 }}>
                <CardContent>
                    <Typography variant="h6" gutterBottom>
                        Upload Contact List
                    </Typography>
                    <Box display="flex" flexDirection="column" gap={2}>
                        <Input type="file" onChange={handleFileChange} />
                        <Button variant="contained" color="primary" onClick={handleUpload}>
                            Upload
                        </Button>
                    </Box>
                </CardContent>
                <Snackbar open={openSnackbar} autoHideDuration={3000} onClose={() => setOpenSnackbar(false)}>
                    <Alert onClose={() => setOpenSnackbar(false)} severity="success" sx={{ width: '100%' }}>
                        File uploaded successfully!
                    </Alert>
                </Snackbar>
            </Card>
        </Dialog>
    );
};

export default DataConnectorPopup;
