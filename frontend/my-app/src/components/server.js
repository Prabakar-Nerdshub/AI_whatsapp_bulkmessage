const express = require("express");
const mongoose = require("mongoose");
const cors = require("cors");
const multer = require("multer");
const XLSX = require("xlsx");
const Papa = require("papaparse");
const fs = require("fs");

const app = express();
app.use(cors());
app.use(express.json());

mongoose.connect("mongodb://localhost:27017/phoneNumbersDB", {
    useNewUrlParser: true,
    useUnifiedTopology: true,
});

const phoneSchema = new mongoose.Schema({
    phoneNumber: String,
});

const PhoneNumber = mongoose.model("PhoneNumber", phoneSchema);

// Multer Setup for File Uploads
const upload = multer({ dest: "uploads/" });

// File Processing and Saving to MongoDB
const extractPhoneNumbers = (filePath, fileType) => {
    return new Promise((resolve, reject) => {
        let phoneNumbers = [];

        if (fileType === "csv") {
            const fileContent = fs.readFileSync(filePath, "utf8");
            Papa.parse(fileContent, {
                header: true,
                complete: (result) => {
                    phoneNumbers = result.data.map(row => row["phone numbers"] || row["Phone"] || row["phone"] || row["Phone Number"]).filter(Boolean);
                    resolve(phoneNumbers);
                },
                error: (err) => reject(err),
            });
        } else if (fileType === "xlsx" || fileType === "xls") {
            const workbook = XLSX.readFile(filePath);
            const sheetName = workbook.SheetNames[0];
            const sheet = workbook.Sheets[sheetName];
            const jsonData = XLSX.utils.sheet_to_json(sheet);
            phoneNumbers = jsonData.map(row => row["phone numbers"] || row["Phone"] || row["phone"] || row["Phone Number"]).filter(Boolean);
            resolve(phoneNumbers);
        } else {
            reject("Invalid file type");
        }
    });
};

// API Route to Handle File Upload
app.post("/upload", upload.single("file"), async (req, res) => {
    try {
        const filePath = req.file.path;
        const fileType = req.file.originalname.split(".").pop().toLowerCase();
        const phoneNumbers = await extractPhoneNumbers(filePath, fileType);

        // Save to MongoDB
        await PhoneNumber.insertMany(phoneNumbers.map(num => ({ phoneNumber: num })));

        // Cleanup: Remove uploaded file
        fs.unlinkSync(filePath);

        res.status(200).json({ message: "File uploaded and data saved successfully!", phoneNumbers });
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: "Error processing file", error });
    }
});

app.listen(5000, () => console.log("Server running on port 5000"));
