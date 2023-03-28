import { useContext } from "react";
import UserInfo from "../components/userInfo";
import AuthContext from "../context/AuthContext";

import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import Grid from '@mui/material/Grid';
import Paper from '@mui/material/Paper';
import Button from '@mui/material/Button';
import Stack from '@mui/material/Stack';
import { Alert, SnackbarContent } from '@mui/material';
import React, { useEffect, useState } from 'react';
import PLayersDrawer from '../components/settingSections/Drawer';
import { Message } from '../components/socket/Message';
import { useHistory } from "react-router-dom";
import { confirmAlert } from 'react-confirm-alert';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemText from '@mui/material/ListItemText';
import Typography from '@mui/material/Typography';
import TextField from '@mui/material/TextField';
import AccountCircle from '@mui/icons-material/AccountCircle';
import SendIcon from '@mui/icons-material/Send';
import Header from "../components/Header";


export default function Home() {
  const [messages, setMessages] = useState([]);
  const [players, setPlayers] = useState([]);
  const [player, setPlayer] = useState({});
  const [message, setMessage] = useState('');
  const { user, socket } = useContext(AuthContext);
  const history = useHistory();
  

  
  useEffect(() => {
    const username = user.sub
    socket.emit('get_player', username, (player) => {
      setPlayer(player)
    })
    socket.on('playerJoined', (data) => {
      setMessages((prevMessages) => [...prevMessages, { ...data, type: 'join'}]);
        const playersList = data.players;
        setPlayers(playersList);
    });

    socket.on('setPlayers', (players) => {
      setPlayers(players)
    });

    socket.on('chat', (messages) => {
      setMessages(messages);
    });
    socket.on('logoutUser', () => {
      localStorage.removeItem("authTokens")
      history.push('/login');
    });

    socket.emit('update_player_session',  username ,(playersList) => {
      setPlayers(playersList);
    });

    socket.emit('get_messages' ,(result) => {
      if (result){
        setMessages(result);
      }
    });

    if (!user.joined) {
      return history.push("/");
    }

    if (user.in_room) {
      return history.push("/tictactoe");
    }

    const hangingRequestPlayer = localStorage.getItem('hanging_request');
    if (hangingRequestPlayer) {
      socket.emit('cancel_request', hangingRequestPlayer);
      localStorage.removeItem('hanging_request');
    }

    const hangingResponsePlayer = localStorage.getItem('hanging_response');
    if (hangingResponsePlayer) {
      socket.emit('decline_request', hangingResponsePlayer);
      localStorage.removeItem('hanging_response');
    }

  }, []);

  console.log("player", player)
  return (
    <div>
      <Header/>
      <Grid container spacing={2} columns={16}>
          <Grid item xs={4}>
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
          <Typography variant="h5">
                    Available players
          </Typography>
              </Paper>
          </Grid >
          </Grid >
            <PLayersDrawer
              avPlayers={players}   
              username={user.sub} 
              socket={socket}
            />
          </Grid>
          <Grid item  xs={12}>
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
              <form>
              <AccountCircle sx={{ color: 'action.active', mr: 1, my: 0.5 }} />
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
                      if (message && message.length && player) {
                        if (player.in_room) {
                          socket.emit('chat_in_room', player.username, message);
                        }else{
                        socket.emit('chat', player.username, message);
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
      </Grid>
    </div>
  );
}


