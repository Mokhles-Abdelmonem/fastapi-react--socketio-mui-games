import * as React from 'react';
import Box from '@mui/material/Box';
import List from '@mui/material/List';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import PersonOutlineIcon from '@mui/icons-material/PersonOutline';
import { useEffect } from 'react';
import { confirmAlert } from 'react-confirm-alert';


export default function PLayersDrawer({avPlayers, username, socket}) {

  const index = avPlayers.indexOf(username);
  if (index > -1) {
    avPlayers.splice(index, 1);
  }
  const handleListItemClick = (event, playerId) => {
    const parent = document.getElementById(playerId);
    const targetPlayer = parent.getElementsByTagName('span')[0].innerHTML;
    if (event.target){
      socket.emit('check_player', targetPlayer, (exist) => {
        if(exist){
          socket.emit('get_rules',(rules) => {
            const gamesLables = ['TicTacToe Game', 'Rock Paper Sessior Game']
            const rulesButtons = rules.map((rule) => {
              return {
                label: `${rule} rule`,
                onClick: () => {
                  const gamesButtons = gamesLables.map((game_type) => {
                    const index = gamesLables.indexOf(game_type)
                    return {
                      label: `${game_type}`,
                      onClick: () => {
                        socket.emit('game_request', username, targetPlayer, rule, index,  () => {
                          localStorage.setItem('hanging_request', targetPlayer)
                          confirmAlert({
                            title: 'Confirm game request',
                            message: `Waiting ${targetPlayer} response`,
                            buttons: [
                              {
                                label: 'Cancel',
                                onClick: () => {
                                  localStorage.removeItem('hanging_request');
                                  socket.emit('cancel_request', targetPlayer);
                                }
                              }
                            ],
                            onClickOutside: () => {
                              localStorage.removeItem('hanging_request');
                              socket.emit('cancel_request', targetPlayer);
                            },
                          });
                        
                        }); 
                      }
                    }
                  });

                  confirmAlert({
                    title: 'Game request',
                    message: `Choose the Game you want to play`,
                    buttons:gamesButtons});
                }
              }
            });
            confirmAlert({
              title: 'Game request',
              message: `Choose the rule for the game (rule number) is the number of winning required to get next level`,
              buttons: rulesButtons
            });
          });
        };

      });
    }
  };

  return (
    <Box sx={{ width: '100%', hight: 360, maxWidth: 360, bgcolor: 'background.paper' }}>
      <List component="nav" aria-label="main mailbox folders">
        {avPlayers.map((username, index) => (
          <ListItemButton
            key={index}
            onClick={(event) => handleListItemClick(event, `player_${username}`)}
          >
            <ListItemIcon>
              <PersonOutlineIcon />
            </ListItemIcon>
            <ListItemText 
            primary={username}
            id={`player_${username}`}
            />
          </ListItemButton>
        ))}
      </List>
    </Box>
  );
}