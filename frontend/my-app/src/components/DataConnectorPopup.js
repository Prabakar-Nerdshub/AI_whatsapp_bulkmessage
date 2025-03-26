import React, { useState, useEffect } from "react";
import axios from "axios";
import {
    Card, CardContent, Typography, Button, Input, Box, TextField,
    Snackbar, Alert, Dialog, LinearProgress, MenuItem, Select, FormControl, InputLabel
} from "@mui/material";

const DataConnectorPopup = ({ open, handleClose }) => {
    const [file, setFile] = useState(null);
    const [fileName, setFileName] = useState(""); // New state for file name
    const [uploadProgress, setUploadProgress] = useState(0);
    const [openSnackbar, setOpenSnackbar] = useState(false);
    const [errorMessage, setErrorMessage] = useState("");
    const [snackbarMessage, setSnackbarMessage] = useState("");
    const [severity, setSeverity] = useState("success");
    const [fileGroups, setFileGroups] = useState([]);
    const [selectedFileGroup, setSelectedFileGroup] = useState("");

    useEffect(() => {
        axios.get(`${CONFIG.API_BASE_URL}/file_groups/`)
            .then((response) => setFileGroups(response.data))
            .catch((error) => console.error("Error fetching file groups:", error));
    }, []);

    const handleFileChange = (e) => {
        const selectedFile = e.target.files[0];
        if (selectedFile) {
            const fileType = selectedFile.name.split('.').pop().toLowerCase();
            if (!['csv', 'xls', 'xlsx'].includes(fileType)) {
                setErrorMessage("Please select a CSV or Excel file.");
                setFile(null);
                return;
            }
            setFile(selectedFile);
            setUploadProgress(0);
        }
    };

    const handleUpload = async () => {
        if (!file || !fileName.trim()) {
            setErrorMessage("Please select a file and enter a name.");
            setSeverity("error");
            setOpenSnackbar(true);
            return;
        }

        const formData = new FormData();
        formData.append("file", file);
        formData.append("file_name", fileName);

        try {
            setUploadProgress(10);
            const response = await axios.post(`${CONFIG.API_BASE_URL}/upload`, formData, {
                headers: { "Content-Type": "multipart/form-data" },
                onUploadProgress: (progressEvent) => {
                    const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total);
                    setUploadProgress(progress);
                }
            });

            if (response.data && response.data.file_id) {
                localStorage.setItem("uploadedFileId", response.data.file_id);
                setSnackbarMessage("File uploaded successfully!");
                setSeverity("success");
                setOpenSnackbar(true);
                setTimeout(() => handleClose(), 1500);
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

    return (
        <Dialog open={open} onClose={handleClose}>
            <Card sx={{ maxWidth: 400, mx: "auto", mt: 4, p: 2, boxShadow: 3 }}>
                <CardContent>
                    <Typography variant="h6" gutterBottom>
                        Upload Contact List
                    </Typography>
                    <Box display="flex" flexDirection="column" gap={2}>
                        <TextField
                            fullWidth
                            variant="outlined"
                            label="File Name"
                            value={fileName}
                            onChange={(e) => setFileName(e.target.value)}
                        />
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
                            disabled={!file || !fileName.trim() || (uploadProgress > 0 && uploadProgress < 100)}
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
            </Card>
        </Dialog>
    );
};

export default DataConnectorPopup;