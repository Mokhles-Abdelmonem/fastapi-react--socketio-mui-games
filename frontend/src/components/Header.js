import React, {useContext, useEffect, useState} from 'react'
import {  useHistory } from 'react-router-dom'
import AuthContext from '../context/AuthContext'
import PropTypes from 'prop-types';
import Toolbar from '@mui/material/Toolbar';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import { confirmAlert } from 'react-confirm-alert';
import { io } from 'socket.io-client';

const socket = io(process.env.REACT_APP_API_URL, {
  path: process.env.REACT_APP_SOCKET_PATH,
});

function Header() {
  const { user, logoutUser } = useContext(AuthContext);
  const [isAdmin , setIsAdmin] = useState(false);
  const [inRoom, setInRoom] = useState(true);
  const username = user.sub
  const history = useHistory();
  const logoutHandler = () => {
    socket.emit('get_player', username,(player) => {   
      console.log('logged out', player)
      if(player.in_room){
        socket.emit('get_opponent', username, player.room_number, (opponent_name) => {   
          if(player.player_won || player.player_lost){
            socket.emit('player_left_room', opponent_name);
            socket.emit('player_logged_out', username, opponent_name);
            logoutUser();
          }else{
            confirmAlert({
              title: 'Attention , you are in the middle of a game',
              message: `logout now will consider loss in game`,
              buttons: [
                {
                  label: 'Logout',
                  onClick: () => {
                    socket.emit('player_left_in_game', opponent_name);
                    socket.emit('player_logged_out', username, opponent_name);
                    logoutUser();
                    
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
        });
        }else{
        socket.emit('player_logged_out', username, null);
        logoutUser();
      }

    });
  };


  const authLinks = (
    <>
          <Button href="/login" variant="outlined" size="small">
              Sign in
          </Button>
          <Button href="/register" variant="outlined" size="small">
              Sign up
          </Button>
    </>
  );

  const settingsLinks = (
    <>
    {
    isAdmin && !inRoom ? 
    (
      <Button href="/admin" variant="outlined" size="small">
        Acount Settings
      </Button>
    ):(
      ''
    )
    }

    <Button onClick={logoutHandler} variant="outlined" size="small">
        logout
    </Button>
    </>
  );

  
  useEffect(() => {
    socket.emit('get_player', username , (player)=> {
      setIsAdmin(player.is_admin);
      setInRoom(player.in_room);
    })
  });

  return (
    <React.Fragment>
      <Toolbar sx={{ borderBottom: 1, borderColor: 'divider' }}>
        <Button href="/" size="small">Socket.io app</Button>
        <Typography
          component="h2"
          variant="h5"
          color="inherit"
          align="center"
          noWrap
          sx={{ flex: 1 }}
        >
          Welcom to Socketio Games {username} 
        </Typography>
        {user ? settingsLinks : authLinks}

      </Toolbar>
    </React.Fragment>
  );
}

export default Header;