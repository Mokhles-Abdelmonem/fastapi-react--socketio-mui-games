import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import CircleIcon from '@mui/icons-material/Circle';
import pawn from '../../images/pawntwo.png'
import pawnBlack from '../../images/pawntwoBlack.png'
import bishop from '../../images/bishoptwo.png'
import bishopBlack from '../../images/bishoptwoBlack.png'
import rook from '../../images/rooktwo.png'
import rookBlack from '../../images/rooktwoBlack.png'
import knight from '../../images/knighttwo.png'
import knightBlack from '../../images/knighttwoBlack.png'
import king from '../../images/goldenking.png'
import kingBlack from '../../images/goldenkingBlack.png'
import queen from '../../images/queentwo.png'
import queenBlack from '../../images/queentwoBlack.png'


export default function Square({
    value, 
    onSquareClick , 
    PieceHighlight, 
    MovesHighlight, 
    chessGame=false,
    RowIndex,
    ColIndex,
    Check,
    playerSide
    }) {
    
    let style={
        fontSize: 30,
        borderRadius: 0,
        maxWidth: '140px',
        maxHeight: '140px',
        minWidth: '140px',
        minHeight: '140px',

    }
    let variant = "h2"
    let newValue = value
    let color = newValue === 'X' ? 'primary' :
    newValue === 'O' ? 'error' : 'info';

    function getPieceValue(newValue) {
        if (newValue === 'P') return <img class="icon_pawn" src={pawn}/>
        if (newValue === 'p') return <img class="icon_pawn" src={pawnBlack}/>
        if (newValue === 'R') return <img class="icon_img" src={rook}/>
        if (newValue === 'r') return <img class="icon_img" src={rookBlack}/>
        if (newValue === 'N') return <img class="icon_img" src={knight}/>
        if (newValue === 'n') return <img class="icon_img" src={knightBlack}/>
        if (newValue === 'B') return <img class="icon_img" src={bishop}/>
        if (newValue === 'b') return <img class="icon_img" src={bishopBlack}/>
        if (newValue === 'Q') return <img class="icon_queen" src={queen}/>
        if (newValue === 'q') return <img class="icon_queen" src={queenBlack}/>
        if (newValue === 'K') return <img class="icon_king" src={king}/>
        if (newValue === 'k') return <img class="icon_king" src={kingBlack}/>
    }
    
    
    if (chessGame) {
        style={
            borderRadius: 0,
            maxWidth: '71px',
            maxHeight: '71px',
            minWidth: '71px',
            minHeight: '71px',
            display: 'inline-flex',
        }
        variant = "h4"
        newValue = getPieceValue(newValue);
        const HighlightPiece = PieceHighlight()
        const HighlightMoves = MovesHighlight()
        if ((RowIndex+ColIndex) % 2 !== 0) {
            color = "primary";
        }
        
        if (HighlightPiece){
            color = "success";
        }
        if (HighlightMoves){
            if (newValue){
                color = "secondary";
            }else{
                newValue = <CircleIcon sx={{fontSize:"20px"}}/>;
            }
        }
        if (Check){
            if(value === Check){
                color = "error";
            } 
        }
    }
    
    return (
    <Button variant="contained" style={style}
        color={color}
        onClick={onSquareClick}>
            <Typography 
            className={playerSide === "player_o" ? ("rotate-element"):("")}
            variant={variant}
            align="center"
            >
                {newValue} 
            </Typography>
        
    </Button>
    );
  }