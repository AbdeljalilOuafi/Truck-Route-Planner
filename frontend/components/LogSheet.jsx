import { Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Typography } from '@mui/material';

const LogSheet = ({ logSheets }) => {
  return (
    <div>
      {logSheets?.map((sheet, sheetIndex) => (
        <Paper key={sheetIndex} sx={{ mb: 2, p: 2 }}>
          <Typography variant="h6" gutterBottom>
            Log Sheet - {sheet.date}
          </Typography>
          
          <TableContainer>
            <Table size="small">
              <TableHead>
                <TableRow>
                  <TableCell>Status</TableCell>
                  <TableCell>Start Time</TableCell>
                  <TableCell>End Time</TableCell>
                  <TableCell>Duration (hrs)</TableCell>
                  <TableCell>Location</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {sheet.activities.map((activity, actIndex) => (
                  <TableRow key={actIndex}>
                    <TableCell>{activity.status}</TableCell>
                    <TableCell>{activity.start_time}</TableCell>
                    <TableCell>{activity.end_time}</TableCell>
                    <TableCell>{activity.duration.toFixed(2)}</TableCell>
                    <TableCell>{activity.location}</TableCell>
                  </TableRow>
                ))}
                <TableRow>
                  <TableCell colSpan={3} align="right">
                    <strong>Total Hours:</strong>
                  </TableCell>
                  <TableCell>
                    <strong>{sheet.total_hours.toFixed(2)}</strong>
                  </TableCell>
                  <TableCell />
                </TableRow>
              </TableBody>
            </Table>
          </TableContainer>
        </Paper>
      ))}
    </div>
  );
};

export default LogSheet;