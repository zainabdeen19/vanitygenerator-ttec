import React, { useState, useEffect } from "react";
import { Grid, List, ListItem, ListItemText } from "@mui/material";
import Accordion from "@mui/material/Accordion";
import AccordionSummary from "@mui/material/AccordionSummary";
import AccordionDetails from "@mui/material/AccordionDetails";
import Typography from "@mui/material/Typography";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import AWS from "aws-sdk";
import dotenv from "dotenv";
dotenv.config();

const MainPage = () => {
  const [phoneNumbers, setPhoneNumbers] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    AWS.config.update({ region: "us-east-1" });
      const dynamodb = new AWS.DynamoDB.DocumentClient();
 	AWS.config.credentials = new AWS.Credentials({
    accessKeyId: process.env.REACT_APP_AWS_ACCESS_KEY_ID,
    secretAccessKey: process.env.REACT_APP_AWS_SECRET_ACCESS_KEY,
  });
      dynamodb.query(
        {
          TableName: "VanityNumber",
          KeyConditionExpression: "PhoneNumber > :number",
          ExpressionAttributeValues: { ":number": "" },
          Limit: 5,
          ScanIndexForward: false,
        },
        (err, data) => {
          if (err) {
            console.error("Unable to query. Error:", JSON.stringify(err, null, 2));
          } else {
            const numbers = data.Items.map((item) => ({
              number: item.PhoneNumber,
              vanityList: item.VanityList,
            }));
            setPhoneNumbers(numbers);
          }
          setIsLoading(false);
        }
      );
 
  }, []);

  return (
    <Grid container spacing={1}>
      <Grid item xs={4}></Grid>
      <Grid
        item
        xs={4}
        style={{
          marginTop: "150px",
          display: "flex",
          flexWrap: "nowrap",
          flexDirection: "row-reverse",
          alignContent: "center",
          justifyContent: "space-evenly",
        }}
      >
        <div>
          {phoneNumbers.map((number) => {
            return (
              <Accordion style={{ width: "150px" }}>
                <AccordionSummary
                  expandIcon={<ExpandMoreIcon />}
                  aria-controls="panel1a-content"
                  id="panel1a-header"
                >
                  <Typography>{number.number}</Typography>
                </AccordionSummary>
                <AccordionDetails>
                  <Typography>
                    <List>
                      {number.vanityList.map((vanity) => {
                        return (
                          <ListItem>
                            <ListItemText>{vanity}</ListItemText>
                          </ListItem>
                        );
                      })}
                    </List>
                  </Typography>
                </AccordionDetails>
              </Accordion>
            );
          })}
        </div>
      </Grid>
      <Grid item xs={4}></Grid>
    </Grid>
  );
};

export default MainPage;
