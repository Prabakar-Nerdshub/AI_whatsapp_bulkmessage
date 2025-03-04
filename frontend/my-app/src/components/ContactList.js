import React, { useEffect, useState } from "react";
import {
    Card,
    CardContent,
    Typography,
    Table,
    TableHead,
    TableBody,
    TableRow,
    TableCell
} from "@mui/material";

const ContactList = () => {
    const [phoneNumbers, setPhoneNumbers] = useState([]);

    useEffect(() => {
        // Retrieve phone numbers from local storage
        const storedNumbers = JSON.parse(localStorage.getItem("uploadedPhoneNumbers")) || [];
        setPhoneNumbers(storedNumbers);
    }, []);

    return (
        <Card sx={{ width: 800, height: 500, mx: "auto", mt: 4, p: 3, boxShadow: 5 }}>
            <CardContent>
                <Typography variant="h5" gutterBottom>
                    Contact List
                </Typography>
                {phoneNumbers.length > 0 ? (
                    <Table>
                        <TableHead>
                            <TableRow>
                                <TableCell sx={{ fontWeight: "bold" }}>S.No</TableCell>
                                <TableCell sx={{ fontWeight: "bold" }}>Phone Number</TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {phoneNumbers.map((number, index) => (
                                <TableRow key={index}>
                                    <TableCell>{index + 1}</TableCell>
                                    <TableCell>{number}</TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                ) : (
                    <Typography variant="body2" color="textSecondary">
                        No contacts uploaded.
                    </Typography>
                )}
            </CardContent>
        </Card>
    );
};

export default ContactList;
