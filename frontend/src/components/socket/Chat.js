import React, { useEffect, useState } from 'react';
import { useHistory } from "react-router-dom";
import { useDispatch, useSelector } from 'react-redux';
import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import Grid from '@mui/material/Grid';
import Paper from '@mui/material/Paper';
import Button from '@mui/material/Button';
import Stack from '@mui/material/Stack';
import { SnackbarContent, Typography } from '@mui/material';

import TextField from '@mui/material/TextField';
import AccountCircle from '@mui/icons-material/AccountCircle';
import SendIcon from '@mui/icons-material/Send';
import { Message } from "./Message";


export default function Chat({socket, level}) {
  const [messages, setMessages] = useState([]);
  const user = useSelector(state => state.auth.user);
  const [message, setMessage] = useState('');


  useEffect(() => {
    if (user) {
    socket.emit('get_chat_messages', user.username ,(result) => {
      if (result){
        setMessages(result);
      }
    });
  }
    
    socket.on('chatInRoom', (messages) => {
      setMessages(messages);
    });


  }, []);
  return (
    <div>
          <Grid item xs={12}>
            <Grid container spacing={2}>

              <Grid item xs={12}>
                <Paper
                  sx={{
                    p: 2,
                    margin: 'auto',
                    maxWidth: 500,
                    flexGrow: 1,
                  }}
                  elevation={24}
                >

                <Container maxWidth="sm">


                <Box sx={{ display: 'flex', alignItems: 'flex-end' }}>

                {level > 1 ? 
                (
                  <form>
                  <AccountCircle sx={{ color: 'action.active', mr: 1, my: 0.5 }} />
                    <span>
                      level {level}
                    </span>
                    <TextField 
                    id="input-with-message" 
                    label="send message" 
                    variant="standard" 
                    onChange={(event) => {
                      const value = event.target.value.trim();
                      setMessage(value);
                    }}
                    />
    
                    <Button 
                      variant="contained"
                      size="large"
                      endIcon={<SendIcon />}
                      onClick={() => {
                          if (message && message.length) {
                            if (user.in_room) {
                              socket.emit('chat_in_room', user.username, message);
                            }
                          }
                          var messageBox = document.getElementById('input-with-message');
                          messageBox.value = '';
                          setMessage('');
                        }
                      }
                      >
                        Send
                    </Button>
                  </form>
    
                ):(
                  <Typography>
                    you are a level {level} player
                    win games in role number to get the next level
                    and be able to chat
                  </Typography>
                )}
                </Box>

                </Container>
              </Paper>
              </Grid>
              <Grid item xs={12}>

                  <Paper
                  sx={{
                    p: 2,
                    margin: 'auto',
                    maxWidth: 500,
                    flexGrow: 1,
                  }}
                  elevation={24}
                >
                  <Container maxWidth="sm">

                  <Box sx={{ 
                    bgcolor: '#e3f2fd',
                    height: '93vh',
                    overflow: 'auto',
                    }}>
                  <Stack spacing={2} sx={{ maxWidth: 600 }}>
                      {messages.map((message, index) => (
                          <SnackbarContent 
                          key={index}
                          sx={{ bgcolor: '#42a5f5' }}
                          message={<Message message={message} />}
                          />
                        ))}

                    </Stack>
                  </Box>
                </Container>
              </Paper>
              </Grid>
            </Grid>

          </Grid>
    </div>
  );
}
