import React from "react";
import { Box, Typography } from "@mui/material";

const Terms = () => {
  return (
    <Box sx={{ padding: 1 }}>
      {/* Terms & Conditions Section */}
      <Typography variant="h4" sx={{ fontWeight: "bold", marginTop: 4 }}>
        Terms & Conditions
      </Typography>

      <Typography variant="h6" sx={{ fontWeight: "bold" }}>1. Acceptance of Terms</Typography>
      <Typography variant="body1">
        By using our services, you agree to these Terms & Conditions. If you do not agree, please do not use our services.
      </Typography>

      <Typography variant="h6" sx={{ fontWeight: "bold", marginTop: 2 }}>2. Services</Typography>
      <Typography variant="body1">
        Nerdshub E PVT LTD provides software development services, including web and mobile app development, custom solutions, and IT consulting.
      </Typography>

      <Typography variant="h6" sx={{ fontWeight: "bold", marginTop: 2 }}>3. User Responsibilities</Typography>
      <ul>
        <li>Users must provide accurate and complete information.</li>
        <li>Unauthorized access or fraudulent activity is strictly prohibited.</li>
      </ul>

      <Typography variant="h6" sx={{ fontWeight: "bold", marginTop: 2 }}>4. Payment & Refund Policy</Typography>
      <ul>
        <li>Payments must be made according to the agreed schedule.</li>
        <li>Refunds are only issued under exceptional circumstances as outlined in individual contracts.</li>
      </ul>

      <Typography variant="h6" sx={{ fontWeight: "bold", marginTop: 2 }}>5. Intellectual Property</Typography>
      <Typography variant="body1">
        All intellectual property, including software, designs, and documentation, developed by Nerdshub E PVT LTD remains our property unless otherwise stated in a written agreement.
      </Typography>

      <Typography variant="h6" sx={{ fontWeight: "bold", marginTop: 2 }}>6. Limitation of Liability</Typography>
      <Typography variant="body1">
        We are not responsible for any direct, indirect, or incidental damages resulting from the use or inability to use our services.
      </Typography>

      <Typography variant="h6" sx={{ fontWeight: "bold", marginTop: 2 }}>7. Termination</Typography>
      <Typography variant="body1">
        We reserve the right to suspend or terminate services if a user violates these terms or engages in unlawful activities.
      </Typography>

      <Typography variant="h6" sx={{ fontWeight: "bold", marginTop: 2 }}>8. Governing Law</Typography>
      <Typography variant="body1">
        These Terms & Conditions are governed by the laws of [Insert Jurisdiction]. Any disputes will be resolved through arbitration or legal proceedings within this jurisdiction.
      </Typography>

      <Typography variant="h6" sx={{ fontWeight: "bold", marginTop: 2 }}>9. Contact Us</Typography>
      <Typography variant="body1">
        For any questions regarding these Terms & Conditions, contact us at [info@nerdshub.co.in].
      </Typography>
    </Box>
  );
};

export default Terms;
