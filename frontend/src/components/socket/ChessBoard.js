import React, { useEffect, useState } from 'react';
import Square from "./Square";
import { useHistory } from "react-router-dom";


export default function ChessBoard({
  socket,
  username,
  board,
  Check,
  handleClick,
  HighlightPiece,
  HighlightMoves
  }) {

  const [playerSide, setPlayerSide] = useState(null);
  const history = useHistory();





  function Board(){
    return (
      <div className="board-row">
        {
        board.map((row, rowIndex) =>(
          row.map((piece, index) =>(
            <Square 
            key={index} 
            value={piece} 
            chessGame={true} 
            PieceHighlight={() => HighlightPiece(rowIndex, index)}
            MovesHighlight={() => HighlightMoves(rowIndex, index)}
            onSquareClick={() => handleClick(rowIndex, index, piece)}
            RowIndex={rowIndex} 
            ColIndex={index} 
            Check={Check}
            playerSide={playerSide}
            />
          ))
        ))
        }
      </div>

    )
  }


  useEffect(() => {

    socket.emit('get_player_side', username ,(result) => {
      setPlayerSide(result);
    });

  }, []);

  return (
    <>
      <div className="status"></div>
      <div className={`board ${playerSide === "player_o" ? ("rotate-element"):("")}`}>
        {Board()}
      </div>
    </>
  );
  }