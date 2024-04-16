import { Box, Stack } from "@mui/material";
import Navbar from "../components/Navbar";

function Homepage () {
  return (
    <Stack direction='column'>
      <Navbar/>
      <Box>
        Hello
      </Box>
    </Stack>
  );
}

export default Homepage;