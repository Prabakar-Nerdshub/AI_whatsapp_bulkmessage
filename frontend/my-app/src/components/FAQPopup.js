import React from "react";
import { DialogTitle, DialogContent, Typography } from "@mui/material";

const faqData = [
  {
    question: "Semak Bantuan",
    answer:
      "Sila layari pautan berikut untuk Semak Status Bantuan anda:\nPautan: https://app.mykasih.net/sara2/checkstatus"
  },
  {
    question: "Senarai Pasaraya",
    answer:
      "Sila layari pautan berikut untuk dapatkan senarai pasaraya terpilih:\nhttps://app.mykasih.net/sara2/merchant-list"
  },
  {
    question: "Program SARA",
    answer:
      "Sumbangan Asas Rahmah (SARA) merupakan program bantuan bersasar kepada rakyat yang paling terkesan dengan kos sara hidup."
  },
  {
    question: "Cara Tebus Bantuan",
    answer:
      "Sila layari pautan berikut untuk mengetahui cara menebus bantuan anda:\nhttps://www.youtube.com/watch?v=hxYmi0OZPEg"
  },
  {
    question: "Mewakilkan Ahli Keluarga",
    answer:
      "Penerima boleh menghantar ahli keluarga sebagai wakil untuk buat pembelian. Sila bawa bersama IC asal penerima semasa tebus bantuan."
  },
  {
    question: "Barang Bantuan",
    answer:
      "Penerima boleh membeli barangan keperluan asas daripada 13 kategori produk yang diluluskan seperti beras, roti, telur, minyak masak, tepung, dll."
  },
  {
    question: "Jumlah Bantuan",
    answer:
      "Penerima akan menerima elaun bulanan melalui MyKad mereka untuk membeli barang keperluan asas terpilih."
  }
];

const FAQPopup = ({ open, handleClose }) => {
    return (
        <>
            <DialogTitle>Frequently Asked Questions</DialogTitle>
            <DialogContent>
                {faqData.map((faq, index) => (
                    <div key={index} style={{ marginBottom: "10px" }}>
                        <Typography variant="h6">{faq.question}</Typography>
                        <Typography variant="body2">{faq.answer}</Typography>
                    </div>
                ))}
            </DialogContent>
        </>
    );
};

export default FAQPopup;
