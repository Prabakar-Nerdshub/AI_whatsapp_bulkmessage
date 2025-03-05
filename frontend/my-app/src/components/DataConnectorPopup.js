import React, { useState } from "react";
import {
    Card, CardContent, Typography, Button, Input, Box,
    Snackbar, Alert, Dialog, LinearProgress
} from "@mui/material";
import axios from "axios";

const DataConnectorPopup = ({ open, handleClose }) => {
    const [file, setFile] = useState(null);
    const [uploadProgress, setUploadProgress] = useState(0);
    const [openSnackbar, setOpenSnackbar] = useState(false);
    const [errorMessage, setErrorMessage] = useState("");
    const [snackbarMessage, setSnackbarMessage] = useState("");
    const [severity, setSeverity] = useState("success");

    // Handle file selection with validation
    const handleFileChange = (e) => {
        const selectedFile = e.target.files[0];
        if (selectedFile) {
            // Check if file is CSV or Excel
            const fileType = selectedFile.name.split('.').pop().toLowerCase();
            if (!['csv', 'xls', 'xlsx'].includes(fileType)) {
                setErrorMessage("Please select a CSV or Excel file.");
                setFile(null);
                return;
            }
            setFile(selectedFile);
            setUploadProgress(0); // Reset progress bar
        }
    };

    // Upload file to MongoDB (GridFS)
    const handleUpload = async () => {
        if (!file) {
            setErrorMessage("Please select a file first.");
            setSeverity("error");
            setOpenSnackbar(true);
            return;
        }

        const formData = new FormData();
        formData.append("file", file);

        try {
            setUploadProgress(10); // Start progress indication

            const response = await axios.post("http://127.0.0.1:8000/api/upload", formData, {
                headers: { "Content-Type": "multipart/form-data" },
                onUploadProgress: (progressEvent) => {
                    const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total);
                    setUploadProgress(progress);
                }
            });

            if (response.data && response.data.file_id) {
                // Store the file ID for use in the Chatbot component
                localStorage.setItem("uploadedFileId", response.data.file_id);

                setSnackbarMessage("File uploaded successfully!");
                setSeverity("success");
                setOpenSnackbar(true);

                // Test that we can retrieve phone numbers
                testPhoneNumberRetrieval(response.data.file_id);
            } else {
                setSnackbarMessage("Upload succeeded but no file ID returned.");
                setSeverity("warning");
                setOpenSnackbar(true);
            }
        } catch (error) {
            console.error("Upload error:", error);
            setSnackbarMessage(error.response?.data?.error || "Error uploading file.");
            setSeverity("error");
            setOpenSnackbar(true);
            setUploadProgress(0);
        }
    };

    // Test that we can retrieve phone numbers from the uploaded file
    const testPhoneNumberRetrieval = async (fileId) => {
        try {
            const response = await axios.get(`http://127.0.0.1:8000/api/get_phone_numbers/${fileId}/`);
            if (response.data && response.data.phone_numbers) {
                const count = response.data.phone_numbers.length;
                setSnackbarMessage(`File uploaded successfully! Found ${count} phone numbers.`);
                setSeverity("success");
                setOpenSnackbar(true);

                // Close dialog after successful verification
                setTimeout(() => handleClose(), 1500);
            }
        } catch (error) {
            console.error("Error retrieving phone numbers:", error);
            setSnackbarMessage("File uploaded but couldn't retrieve phone numbers.");
            setSeverity("warning");
            setOpenSnackbar(true);
        }
    };

    // Close snackbar
    const handleSnackbarClose = () => {
        setOpenSnackbar(false);
    };

    return (
        <Dialog open={open} onClose={handleClose}>
            <Card sx={{ maxWidth: 400, mx: "auto", mt: 4, p: 2, boxShadow: 3 }}>
                <CardContent>
                    <Typography variant="h6" gutterBottom>
                        Upload Contact List
                    </Typography>
                    <Box display="flex" flexDirection="column" gap={2}>
                        <Input
                            type="file"
                            onChange={handleFileChange}
                            inputProps={{ accept: ".csv,.xls,.xlsx" }}
                        />
                        {file && (
                            <Typography variant="body2" color="textSecondary">
                                Selected file: {file.name}
                            </Typography>
                        )}
                        <Button
                            variant="contained"
                            color="primary"
                            onClick={handleUpload}
                            disabled={!file || uploadProgress > 0 && uploadProgress < 100}
                        >
                            Upload
                        </Button>
                        {uploadProgress > 0 && (
                            <Box sx={{ width: '100%', mt: 2 }}>
                                <LinearProgress variant="determinate" value={uploadProgress} />
                                <Typography variant="body2" align="center" sx={{ mt: 1 }}>
                                    {uploadProgress}%
                                </Typography>
                            </Box>
                        )}
                    </Box>
                </CardContent>
                <Snackbar
                    open={openSnackbar}
                    autoHideDuration={5000}
                    onClose={handleSnackbarClose}
                >
                    <Alert
                        onClose={handleSnackbarClose}
                        severity={severity}
                        sx={{ width: '100%' }}
                    >
                        {snackbarMessage}
                    </Alert>
                </Snackbar>
            </Card>
        </Dialog>
    );
};

export default DataConnectorPopup;