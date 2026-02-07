import React from "react";
import {
  Card,
  CardContent,
  Typography,
  Button,
  Box,
  Divider,
  Stack,
} from "@mui/material";
import ReactMarkdown from "react-markdown";
import { jsPDF } from "jspdf";
import DownloadIcon from "@mui/icons-material/Download";
import PictureAsPdfIcon from "@mui/icons-material/PictureAsPdf";

export default function Report({ data }) {
  if (!data) return null;

  // Global cleaning function for exports
  const getCleanText = (raw) => {
    return raw
      .replace(/â‚¦/g, "NGN") // CRITICAL: Fix encoding jargon
      .replace(/[#*`_~]/g, "") // Strip Markdown for PDF/TXT
      .trim();
  };

  const downloadTxt = () => {
    const element = document.createElement("a");
    const file = new Blob([getCleanText(data)], { type: "text/plain" });
    element.href = URL.createObjectURL(file);
    element.download = "Investment_Report.txt";
    document.body.appendChild(element);
    element.click();
  };

  const downloadPdf = () => {
    const doc = new jsPDF();
    const pageWidth = doc.internal.pageSize.getWidth();
    const margin = 20;
    const contentWidth = pageWidth - margin * 2;
    let yPos = 30;

    // Header - Binary Intelligence Branding
    doc.setFillColor(30, 41, 59);
    doc.rect(0, 0, pageWidth, 40, "F");
    doc.setTextColor(255, 255, 255);
    doc.setFont("helvetica", "bold");
    doc.setFontSize(20);
    doc.text("BINARY INTELLIGENCE", margin, 25);

    yPos = 55;
    doc.setTextColor(60, 60, 60);

    // Split and render lines with the cleaned NGN text
    const rawLines = data.split("\n");
    rawLines.forEach((line) => {
      if (!line.trim()) {
        yPos += 5;
        return;
      }

      doc.setFont("helvetica", line.startsWith("#") ? "bold" : "normal");
      doc.setFontSize(line.startsWith("#") ? 14 : 10);

      const cleanLine = getCleanText(line);
      const splitLines = doc.splitTextToSize(cleanLine, contentWidth);

      splitLines.forEach((textLine) => {
        if (yPos > 275) {
          doc.addPage();
          yPos = 20;
        }
        doc.text(textLine, margin, yPos);
        yPos += 7;
      });
      yPos += 2;
    });

    doc.save("Binary_Investment_Report.pdf");
  };

  return (
    <Card className="glass-card" sx={{ mt: 4, borderRadius: "24px" }}>
      <CardContent sx={{ p: 4 }}>
        <Box
          display="flex"
          justifyContent="space-between"
          alignItems="center"
          mb={3}
        >
          <Typography
            variant="h5"
            sx={{ fontWeight: 800, color: "var(--accent)" }}
          >
            Analysis Report
          </Typography>
          <Stack direction="row" spacing={1}>
            <Button
              size="small"
              variant="outlined"
              startIcon={<DownloadIcon />}
              onClick={downloadTxt}
            >
              TXT
            </Button>
            <Button
              size="small"
              variant="contained"
              startIcon={<PictureAsPdfIcon />}
              onClick={downloadPdf}
              sx={{ background: "var(--accent)" }}
            >
              PDF
            </Button>
          </Stack>
        </Box>
        <Divider sx={{ mb: 3 }} />
       <Box
  sx={{
    lineHeight: 1.9,
    // Target all markdown elements to inherit the color from Typography
    "& *": {
      color: "inherit !important",
    },
  }}
>
  <Typography component="div" sx={{ color: "text.primary" }}>
    <ReactMarkdown>{data}</ReactMarkdown>
  </Typography>
</Box>
      </CardContent>
    </Card>
  );
}