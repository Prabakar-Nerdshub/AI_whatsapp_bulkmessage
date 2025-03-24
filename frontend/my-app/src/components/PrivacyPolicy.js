import React from "react";
import { Box, Typography } from "@mui/material";

const PrivacyPolicy = () => {
  return (
    <Box sx={{ padding: 4 }}>
      {/* Privacy Policy Section */}
      <Typography variant="h4" sx={{ fontWeight: "bold", marginBottom: 2 }}>
        Privacy Policy
      </Typography>

      <Typography variant="h6" sx={{ fontWeight: "bold" }}>1. Introduction</Typography>
      <Typography variant="body1">
        Nerdshub E PVT LTD ("Company," "we," "us," or "our") values your privacy. This Privacy Policy describes how we collect, use, and protect your personal information when using our services.
      </Typography>

      <Typography variant="h6" sx={{ fontWeight: "bold", marginTop: 2 }}>2. Information We Collect</Typography>
      <Typography variant="body1">
        We may collect the following types of personal and non-personal information:
      </Typography>
      <ul>
        <li>Name, email address, phone number, and contact details</li>
        <li>Payment and billing information</li>
        <li>IP address, device type, and browsing behavior</li>
        <li>Data provided by clients for software development</li>
      </ul>

      <Typography variant="h6" sx={{ fontWeight: "bold", marginTop: 2 }}>3. How We Use Your Information</Typography>
      <ul>
        <li>To provide, operate, and maintain our services</li>
        <li>To process payments and manage client accounts</li>
        <li>To communicate updates and service-related information</li>
        <li>To comply with legal and regulatory obligations</li>
      </ul>

      <Typography variant="h6" sx={{ fontWeight: "bold", marginTop: 2 }}>4. Data Sharing & Protection</Typography>
      <Typography variant="body1">
        We do not sell or rent personal data. We may share information with trusted third parties, such as payment processors, under strict confidentiality agreements.
      </Typography>

      <Typography variant="h6" sx={{ fontWeight: "bold", marginTop: 2 }}>5. Your Rights</Typography>
      <Typography variant="body1">
        You have the right to:
      </Typography>
      <ul>
        <li>Access, update, or delete your personal data</li>
        <li>Opt-out of marketing communications</li>
        <li>Request details about how your data is used</li>
      </ul>
      <Typography variant="body1">
        To exercise these rights, contact us at [Insert Contact Details].
      </Typography>

      <Typography variant="h6" sx={{ fontWeight: "bold", marginTop: 2 }}>6. Changes to This Privacy Policy</Typography>
      <Typography variant="body1">
        We may update this Privacy Policy from time to time. Any changes will be posted on this page with the updated effective date.
      </Typography>

      <Typography variant="h6" sx={{ fontWeight: "bold", marginTop: 2 }}>7. Contact Us</Typography>
      <Typography variant="body1">
        For questions regarding this Privacy Policy, contact us at [info@nerdshub.co.in].
      </Typography>
    </Box>
  );
};

export default PrivacyPolicy;
