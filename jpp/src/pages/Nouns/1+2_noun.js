import { Box } from "@mui/material";
import React from "react";
import Recorder from "../../components/Recorder";
import WordBank from "../../components/Wordbank";

function OneTwoNoun () {
  return (
    <Box id="mw">
      <Recorder></Recorder>
      <WordBank></WordBank>
    </Box>
  );
}

export default OneTwoNoun;