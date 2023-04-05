import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import CircleIcon from '@mui/icons-material/Circle';


export default function Square({ value, onSquareClick , PieceHighlight, MovesHighlight, chessGame=false}) {
    
    let style={
        fontSize: 30,
        borderRadius: 0,
        maxWidth: '140px',
        maxHeight: '140px',
        minWidth: '140px',
        minHeight: '140px'
    }
    let variant = "h2"
    
    let color = value === 'X' ? 'primary' :
    value === 'O' ? 'error' : 'info';

    function getPieceValue(value) {
        if (value === 'P') return <img src="https://img.icons8.com/ios/35/null/pawn.png"/>
        if (value === 'p') return <img src="https://img.icons8.com/ios-filled/35/null/pawn.png"/>
        if (value === 'R') return <img src="https://img.icons8.com/ios/35/null/rook.png"/>
        if (value === 'r') return <img src="https://img.icons8.com/ios-filled/35/null/rook.png"/>
        if (value === 'N') return <img src="https://img.icons8.com/ios/35/null/knight.png"/>
        if (value === 'n') return <img src="https://img.icons8.com/ios-filled/35/null/knight.png"/>
        if (value === 'B') return <img src="https://img.icons8.com/ios/35/null/bishop.png"/>
        if (value === 'b') return <img src="https://img.icons8.com/ios-filled/35/null/bishop.png"/>
        if (value === 'Q') return <img src="https://img.icons8.com/ios/35/null/queen.png"/>
        if (value === 'q') return <img src="https://img.icons8.com/ios-filled/35/null/queen.png"/>
        if (value === 'K') return <img src="https://img.icons8.com/ios/35/null/king.png"/>
        if (value === 'k') return <img src="https://img.icons8.com/ios-filled/35/null/king.png"/>

    }
    
    if (chessGame) {
        style={
            fontSize: 15,
            borderRadius: 0,
            maxWidth: '50px',
            maxHeight: '50px',
            minWidth: '50px',
            minHeight: '50px'
        }
        variant = "h4"
        value = getPieceValue(value);
        const HighlightPiece = PieceHighlight()
        const HighlightMoves = MovesHighlight()
        if (HighlightMoves){
            value = <CircleIcon sx={{fontSize:"20px"}}/>;
        }
        if (HighlightPiece){
            color = "success";
        }
        
    }
    
    return (
    <Button variant="contained" style={style}
        color={color}
        onClick={onSquareClick}>
            <Typography variant={variant}>
                {value} 
            </Typography>
        
    </Button>
    );
  }