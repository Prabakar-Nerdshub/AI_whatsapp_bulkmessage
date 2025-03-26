import React, { useState } from "react";
import DataConnectorPopup from "./DataConnectorPopup";
import { Button } from "@mui/material";

const ParentComponent = () => {
  const [open, setOpen] = useState(false);

  const handleFileUpload = (file) => {
    console.log("Uploaded file:", file);
    setOpen(false); // ✅ Close after upload
  };

  return (
    <>
      <Button variant="contained" onClick={() => setOpen(true)}>
        Open Data Connector
      </Button>

      <DataConnectorPopup open={open} setOpen={setOpen} onFileUpload={handleFileUpload} />
    </>
  );
};

export default ParentComponent;
