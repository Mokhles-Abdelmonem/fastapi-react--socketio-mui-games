import Square from "./Square";
import ReceiptIcon from '@mui/icons-material/Receipt';
import ContentCutIcon from '@mui/icons-material/ContentCut';
import CircleIcon from '@mui/icons-material/Circle';



export default function RPSBoard({Clicked, handleClick}) {
    const clickedSquare = (Clicked) => {
      if (Clicked === 0) return <Square value={<CircleIcon sx={{fontSize:"50px"}}/>} /> 
      if (Clicked === 1) return <Square value={<ReceiptIcon sx={{fontSize:"50px"}}/>} /> 
      if (Clicked === 2) return <Square value={<ContentCutIcon sx={{fontSize:"50px"}}/>} /> 
    }
  

    return (
      <>
        <div className="status"></div>
        <div className="board">
            <div className="board-row">
              {
                Clicked || Clicked === 0 ? (
                    <>
                    {clickedSquare(Clicked)}
                    </>
                  ):(
                    <>
                    <Square value={<CircleIcon sx={{fontSize:"50px"}}/>} onSquareClick={() => handleClick(0)} />
                    <Square value={<ReceiptIcon sx={{fontSize:"50px"}}/>} onSquareClick={() => handleClick(1)} />
                    <Square value={<ContentCutIcon sx={{fontSize:"50px"}}/>} onSquareClick={() => handleClick(2)} />
                    </>
                    )
              }
            </div>
        </div>

      </>
    );
  }