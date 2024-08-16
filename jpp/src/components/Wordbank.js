import { Box, Grid } from "@mui/material";
import { useEffect, useState } from "react";
import axios from 'axios';

function WordBank() {
  const [words, setWords] = useState();

  async function parseData(txt) {
    setWords(txt);
  }

  useEffect(() => {
    async function fetchData() {
      const response = await axios.get('http://localhost:3000/words/1+2noun.txt');
      await parseData(response.data);
    }
    fetchData()
  }, []);

  // console.log(words)

  return (
    <Box>
      <Grid container spacing={{ xs: 2, md: 3 }} columns={{ xs: 4, sm: 8, md: 12 }}>
        {Array.from(Array(12)).map((_, index) => (
          <Grid item xs={2} sm={4} md={4} key={index}>
            <Box>H</Box>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
}

export default WordBank;