import { useContext } from "react";
import AuthContext from "../context/AuthContext";
import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import Grid from '@mui/material/Grid';
import Paper from '@mui/material/Paper';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import React, { useEffect, useState } from 'react';

import { Redirect, useHistory } from "react-router-dom";
import useWindowSize from "@rooks/use-window-size"
import Confetti from 'react-confetti'
import { confirmAlert } from 'react-confirm-alert';


import Board from '../components/socket/Board';
import Chat from '../components/socket/Chat';
import RPSBoard from '../components/socket/RPSBoard';
import Header from "../components/Header";




export default function Game() {
  const [opponentName, setOpponentName] = useState('');
  const [Room, setRoom] = useState('');

  const [timer, setTimer] = useState('');
  
  const [playerWon, setPlayerWon] = useState(false);
  const [playerLost, setPlayerLost] = useState(false);
  const [playerDraw, setPlayerDraw] = useState(false);


  const [board, setBoard] = useState([Array(9).fill(null)]);

  const [Clicked, setClicked] = useState(null);

  const { user, socket } = useContext(AuthContext);
  const username = user.sub

  const { innerWidth, innerHeight, outerHeight, outerWidth } = useWindowSize();
  let browserHistory = useHistory();

  const [level, setLevel] = useState(0);
  const [game, setGame] = useState(null);


  const leaveAction  = () => {
    if (playerWon || playerLost || playerDraw){
      socket.emit('player_left_room', opponentName);
      socket.emit('leave_room', user, (result) => {
        browserHistory.push("/dashboard") 
      });
    }else{
      confirmAlert({
        title: 'Attention , you are in the middle of a game',
        message: `leaving the game will consider loss`,
        buttons: [
          {
            label: 'leave',
            onClick: () => {
              socket.emit('player_left_in_game', opponentName);
              socket.emit('leave_room', user, (result) => {
                browserHistory.push("/dashboard") 
              });
            }
          },
          {
            label: 'Stay',
            onClick: () => {
            }
          }
        ]
      });
    }

  }

  const handelRemach  = () => {
    console.log('handelRemach called');
    socket.emit('rematch_game', Room);
  }

  function handleClick(i) {
    socket.emit('handle_click', i, username);
  }

  function handleRPSClick(i) {
    socket.emit('handle_rps_click', i, username, opponentName,(res)=>{
    if(res){
      setClicked(i);
    } 
    });
  }


  useEffect(() => {

    socket.emit('update_player_session',  username ,(result) => {
      const player = result.player;
      setPlayerWon(player.player_won);
      setPlayerLost(player.player_lost);
      setPlayerDraw(player.player_draw);
      setLevel(player.level);
      setRoom(player.room_number);
    });

    socket.emit('get_board', username ,(result) => {
      setBoard(result);
    });

    socket.on('setTimer', (timer) => {
      console.log('setTimer', timer)
      setTimer(timer);
    });

    socket.on('congrateWinner', (level) => {
      setPlayerWon(true);
      setLevel(level);
    });

    socket.on('noteOpponent', (level) => {
      setPlayerLost(true);
      setLevel(level);
      confirmAlert({
        title: 'Sorry you Lost',
        message: `your can win next time`,
        buttons: [
          {
            label: 'Ok',
            onClick: () => {
            }
          }
        ]
      });
    });

    socket.on('setBoard', (res) => {
      setBoard(res);
    });

    socket.on('rematchGame', () => {
      setPlayerWon(false);
      setPlayerLost(false);
      setPlayerDraw(false);
      setBoard([Array(9).fill(null)]);
      setClicked(null);
      socket.emit('get_user_level', username ,(level) => {
          setLevel(level)
      });
    });
    
  }, []);


  return (
    <div>
      {playerWon ? (    
      <Confetti
      width={outerWidth}
      height={outerHeight}
      />
    ):('')}
    <Header/>
    <Box  sx={{ width: '100%' }}>
      <Grid container rowSpacing={1} columnSpacing={{ xs: 1, sm: 2, md: 3 }}>
        <Grid item xs={6} md={4}>
          <Chat
          socket={socket}
          level={level}
          />
        </Grid>
        <Grid item xs={6} md={8}>
        <Grid container spacing={2}>

        <Grid item xs={16}>
              <Paper
                sx={{
                  p: 2,
                  margin: 'auto',
                  maxWidth: 500,
                  flexGrow: 1,
                }}
                elevation={24}
              >
                <Grid
                  container
                  spacing={0}
                  direction="column"

                >
                {playerWon || playerLost || playerDraw? (    
                <Button 
                variant="outlined"
                color="primary"
                onClick={handelRemach}
                >
                  rematch
                </Button>
                ):('')}
                <Button 
                variant="outlined"
                color="error"
                onClick={leaveAction}
                >
                  leave
                </Button>
                </Grid>
            </Paper>
          </Grid>
          <Grid item xs={16}>
            <Grid container spacing={2}>

            <Grid item xs={16}>

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

                  <Box sx={{ bgcolor: '#e3f2fd', minHeight: '10vh' }}>
                  <Grid
                    container
                    spacing={0}
                    direction="column"
                    alignItems="center"
                    justifyContent="center"
                  >

                    <Typography variant="h2" gutterBottom>
                      {timer ? timer: '00:15'}
                    </Typography>
                    
                  </Grid>
                  </Box>
                </Container>
              </Paper>
              </Grid>
              <Grid item xs={16}>
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
                  <Box sx={{ minHeight: '50vh' }}>
                    <div className='game'>
                      {game === 1 ? (
                        <RPSBoard
                        Clicked={Clicked}
                        handleClick={handleRPSClick}
                        />
                      ):(
                        <Board
                        squares={board}
                        handleClick={handleClick}
                        />
                      ) }

                    </div>
                  </Box>

                </Container>
              </Paper>
            </Grid>
            </Grid>
          </Grid>
        </Grid>

        </Grid>
      </Grid>
    </Box>
    </div>
  );
}
