import React, { useEffect, useState } from 'react';
import Square from "./Square";

export default function ChessBoard({socket, username}) {

  const [board, setChessBoard] = useState([Array(9).fill(null)]);

  function handleClick(rowIndex, index, piece){
    if (piece === " ") return;
    socket.emit("handle_chess_click", username, rowIndex, index, piece)
    console.log("rowIndex", rowIndex);
    console.log("index", index);
    console.log("piece", piece);
  }

  function Board(){
    return (
      <div className="board-row">
        {
        board.map((row, rowIndex) =>(
          row.map((piece, index) =>(
            <Square key={index} value={piece} chessGame={true} onSquareClick={() => handleClick(rowIndex, index, piece)} />
          ))
        ))
        }
      </div>

    )
  }


  useEffect(() => {

    socket.emit('get_chess_board', username ,(result) => {
      setChessBoard(result);
    });

  }, []);

  return (
    <>
      <div className="status"></div>
      <div className="board">
        {Board()}
      </div>
    </>
  );
  }