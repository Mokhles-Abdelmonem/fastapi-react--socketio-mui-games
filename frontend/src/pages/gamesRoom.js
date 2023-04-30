import { useContext } from "react";
import AuthContext from "../context/AuthContext";
import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import Grid from '@mui/material/Grid';
import Paper from '@mui/material/Paper';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import React, { useEffect, useState } from 'react';

import { useHistory } from "react-router-dom";
import useWindowSize from "@rooks/use-window-size"
import Confetti from 'react-confetti'
import { confirmAlert } from 'react-confirm-alert';


import Board from '../components/socket/Board';
import Chat from '../components/socket/Chat';
import RPSBoard from '../components/socket/RPSBoard';
import Header from "../components/Header";
import ChessBoard from "../components/socket/ChessBoard";




export default function Game() {
  const [opponentName, setOpponentName] = useState('');
  const [Room, setRoom] = useState('');

  const [timer, setTimer] = useState('');
  
  const [playerWon, setPlayerWon] = useState(false);
  const [playerLost, setPlayerLost] = useState(false);
  const [playerDraw, setPlayerDraw] = useState(false);


  const [board, setBoard] = useState([Array(9).fill(null)]);

  const [Clicked, setClicked] = useState(null);

  const { user, socket, logoutUser } = useContext(AuthContext);
  const username = user.sub

  const { innerWidth, innerHeight, outerHeight, outerWidth } = useWindowSize();
  const history = useHistory();

  const [level, setLevel] = useState(0);
  const [game, setGame] = useState(null);

  const [highlightMoves, setHighlightMoves] = useState([]);
  const [highlightPiece, setHighlightPiece] = useState([]);
  const [chessBoard, setChessBoard] = useState([Array(9).fill(null)]);
  const [Check, setCheck] = useState(null);

  const [drawRequest, setDrawRequest] = useState(false);







  function highlightClicked(rowIndex, index){
    if( highlightMoves.length > 0 ){
      for( let i = 0; i < highlightMoves.length; i++){
        if (
          highlightMoves[i][0] === rowIndex &&
          highlightMoves[i][1] === index
        ){
          return true;
        } 
      }
      return false;
    }
    
  }

  function handleChessClick(rowIndex, index, piece){
    const highlClicked = highlightClicked(rowIndex, index)
    if(highlClicked) {
      const initRowIndex = highlightPiece[0]
      const initIndex = highlightPiece[1]
      socket.emit("submit_piece_move", username, rowIndex, index, initRowIndex, initIndex)
    }
    setHighlightPiece([]);
    setHighlightMoves([]);
    socket.emit("get_available_moves", username, rowIndex, index, piece, (result)=>{
      if (result){
        setHighlightPiece(result.highlightPiece);
        setHighlightMoves(result.available_moves);
      }
    })
  };




  function HighlightMoves(rowIndex, index){
    for (let i = 0; i < highlightMoves.length; i++ ){
      if (rowIndex === highlightMoves[i][0] && index === highlightMoves[i][1]){
        return true;
      }
    }
    return false;
  };


  function HighlightPiece(rowIndex, index){
      if (rowIndex === highlightPiece[0] && index === highlightPiece[1]){
        return true;
      }
    return false;
  };


  function handleDrawRequest() {
    socket.emit('handle_draw_request', opponentName);
  }

  function handleDrawAccept() {
    socket.emit('handle_draw_accept', username, Room,opponentName);
  }

  function handleDrawDecline() {
    socket.emit('handle_draw_decline', username);
    setDrawRequest(false);
  }

  function DrawButton(request=false){
    
    if (request) {
      return (
        <Grid
          container
        >
        <Button 
          color="primary"
        >
          {`draw request >>>`}
        </Button>
        <Button 
          variant="contained"
          color="success"
          onClick={handleDrawAccept}
        >
          accept draw
        </Button>
        <Button 
          variant="contained"
          color="error"
          onClick={handleDrawDecline}
        >
          decline draw
        </Button>
        </Grid>
      
      )
    }else{
      return(
        <Button 
        variant="outlined"
        color="success"
        onClick={handleDrawRequest}
        >
          request draw 
        </Button>
      )}
    }

    






  const leaveAction  = () => {
    if (playerWon || playerLost || playerDraw){
      socket.emit('player_left_room', opponentName);
      socket.emit('leave_room', username, opponentName, ()=>{
        history.push("/")
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
              socket.emit('leave_room', username, opponentName, ()=>{
                history.push("/")
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
    socket.emit('rematch_game', Room);
  }

  function handleClick(i) {
    socket.emit('handle_click', i, username);
  }

  function handleRPSClick(i) {
    socket.emit('handle_rps_click', i, username, opponentName, Room,(res)=>{
    if(res){
      setClicked(i);
    } 
    });
  }

  socket.on('notePlayerLeft', () => {
    history.push("/") 
    confirmAlert({
      title: 'your opponent left the game',
      message: `the room is empty now, we redirected you home page`,
      buttons: [
        {
          label: 'Ok',
          onClick: () => {

          }
        }
      ],
      onClickOutside: () => {
      },
    });
  });


  useEffect(() => {

    socket.emit('update_player_session',  username ,(result) => {
      const player = result.player;
      const opponent_name = result.opponent_name
      setPlayerWon(player.player_won);
      setPlayerLost(player.player_lost);
      setPlayerDraw(player.player_draw);
      setDrawRequest(player.draw_request);
      setLevel(player.level);
      setRoom(player.room_number);
      setOpponentName(opponent_name);
      if(!player.in_room) history.push("/")
    });

    socket.emit('get_board', username ,(result) => {
      setBoard(result);
    });

    socket.emit('get_game', username ,(result) => {
      setGame(result);
    });

    socket.on('setTimer', (timer) => {
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


    socket.on('noteOpponentWon', () => {
      history.push("/")
      confirmAlert({
        title: 'Congrates you won',
        message: `your opponent leaved the game , you daclared as winner`,
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
      setDrawRequest(false);
      setBoard([Array(9).fill(null)]);
      setClicked(null);
      setHighlightPiece([]);
      setHighlightMoves([]);
      socket.emit('get_user_level', username ,(level) => {
          setLevel(level)
      });
      socket.emit('get_chess_board', username ,(result) => {
        setChessBoard(result.chess_board);
        setCheck(result.check);
      });
    });

    socket.on('declareDraw', () => {
      setPlayerDraw(true);
      confirmAlert({
        title: 'Tie ',
        message: `the game settled to draw, your can win next time`,
        buttons: [
          {
            label: 'Ok',
            onClick: () => {
            }
          }
        ]
      });
    });

    socket.on('logeUserOut',  ()  => {
      logoutUser();
    });


    socket.emit('get_chess_board', username ,(result) => {
      setChessBoard(result.chess_board);
      setCheck(result.check);
    });

    socket.on('setChessBoard', (board) => {
      setChessBoard(board);
    });



    socket.on('setCheck', (King) => {
      setCheck(King);
    });

    socket.on('PawnPermotion', (cordinates) => {
      const r_index = cordinates[0];
      const c_index = cordinates[1];
      const initial_r_index = cordinates[2];
      const initial_c_index = cordinates[3];
      const PermotionList = ["Queen", "Rook", "Bishop", "Knight"]
      const buttons = PermotionList.map((piece) => {
        return {
          label: `${piece}`,
          onClick: () => {
            socket.emit('permote_pawn', username, piece, r_index, c_index, initial_r_index, initial_c_index); 
          }
        }});
      confirmAlert({
        title: 'Tie ',
        message: `the game settled to draw, your can win next time`,
        buttons: buttons
      });
    });


    socket.on('setDrawRequest', (request) => {
      setDrawRequest(request);
    });

  }, []);


  function getGameBoard(){
    if (game === 0) return <Board squares={board} handleClick={handleClick}/>
    if (game === 1) return <RPSBoard Clicked={Clicked} handleClick={handleRPSClick}/>
    if (game === 2) return <ChessBoard 
    socket={socket} 
    username={username}
    board={chessBoard}
    Check={Check}
    handleClick={handleChessClick}
    HighlightPiece={HighlightPiece}
    HighlightMoves={HighlightMoves}
    />
  } 

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
      <Grid container sx={{ width: '100%' }}>
        <Grid item xs={4} >
          <Chat
          socket={socket}
          level={level}
          />
        </Grid>
        <Grid item xs={8} >
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
                  ):(
                    DrawButton(drawRequest)
                  )}
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
                            {timer ? timer: '--:--'}
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
                      minHeight: 500,
                      maxHeight: 600,
                      minWidth: 500,
                      maxWidth: 600,
                      flexGrow: 1,
                    }}
                    elevation={24}
                  >
                      <Box sx={{ 
                        display:"flex" 
                        }}>
                        <div className='game'>
                          {getGameBoard()}
                        </div>
                      </Box>
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
