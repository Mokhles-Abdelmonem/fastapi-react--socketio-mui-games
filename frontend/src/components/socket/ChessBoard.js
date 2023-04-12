import React, { useEffect, useState } from 'react';
import Square from "./Square";
import { useHistory } from "react-router-dom";


export default function ChessBoard({socket, username}) {

  const [board, setChessBoard] = useState([Array(9).fill(null)]);
  const [Check, setCheck] = useState(null);
  const [highlightMoves, setHighlightMoves] = useState([]);
  const [highlightPiece, setHighlightPiece] = useState([]);
  const history = useHistory();

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

  function handleClick(rowIndex, index, piece){
    const highlClicked = highlightClicked(rowIndex, index)
    if(highlClicked) {
      const initRowIndex = highlightPiece[0]
      const initIndex = highlightPiece[1]
      console.log("init Highlight Piece >>>>>>>>>> ",[initRowIndex, initIndex]  )
      socket.emit("submit_piece_move", username, rowIndex, index, initRowIndex, initIndex)
    }
    setHighlightPiece([]);
    setHighlightMoves([]);
    socket.emit("get_available_moves", username, rowIndex, index, piece, (result)=>{
      console.log("current index >>>>>>>>>> ",rowIndex, index  )
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
            />
          ))
        ))
        }
      </div>

    )
  }


  useEffect(() => {
    socket.emit('update_player_session',  username ,(result) => {
      const player = result.player;
      if(!player.in_room) history.push("/")
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