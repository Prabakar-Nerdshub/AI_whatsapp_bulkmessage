import React, { useEffect, useState } from "react";
import { Card, CardContent, Typography, Table, TableHead, TableBody, TableRow, TableCell } from "@mui/material";

const GroupedContacts = () => {
    const [groupedContacts, setGroupedContacts] = useState({});

    useEffect(() => {
        const storedContacts = JSON.parse(localStorage.getItem("uploadedContacts")) || [];

        const grouped = storedContacts.reduce((acc, contact, index) => {
            if (!acc[contact.area]) {
                acc[contact.area] = [];
            }
            acc[contact.area].push(contact);
            return acc;
        }, {});

        setGroupedContacts(grouped);
    }, []);

    return (
        <Card sx={{ width: 800, mx: "auto", mt: 4, p: 3 }}>
            <CardContent>
                <Typography variant="h5"></Typography>
                {Object.entries(groupedContacts).map(([area, contacts], index) => (
                    <div key={index}>
                        <Typography variant="h6">{`Group ${index + 1}: ${area}`}</Typography>
                        <Table>
                            <TableHead>
                                <TableRow>
                                    <TableCell>Name</TableCell>
                                    <TableCell>Phone Number</TableCell>
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                {contacts.map((contact, idx) => (
                                    <TableRow key={idx}>
                                        <TableCell>{contact.name}</TableCell>
                                        <TableCell>{contact.phoneNumber}</TableCell>
                                    </TableRow>
                                ))}
                            </TableBody>
                        </Table>
                    </div>
                ))}
            </CardContent>
        </Card>
    );
};

export default GroupedContacts;
