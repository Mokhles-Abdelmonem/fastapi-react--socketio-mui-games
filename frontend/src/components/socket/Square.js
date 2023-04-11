import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import CircleIcon from '@mui/icons-material/Circle';


export default function Square({
    value, 
    onSquareClick , 
    PieceHighlight, 
    MovesHighlight, 
    chessGame=false,
    RowIndex,
    ColIndex,
    Check
    }) {
    
    let style={
        fontSize: 30,
        borderRadius: 0,
        maxWidth: '140px',
        maxHeight: '140px',
        minWidth: '140px',
        minHeight: '140px'
    }
    let variant = "h2"
    let newValue = value
    let color = newValue === 'X' ? 'primary' :
    newValue === 'O' ? 'error' : 'info';

    function getPieceValue(newValue) {
        if (newValue === 'P') return <img src="https://img.icons8.com/ios/35/null/pawn.png"/>
        if (newValue === 'p') return <img src="https://img.icons8.com/ios-filled/35/null/pawn.png"/>
        if (newValue === 'R') return <img src="https://img.icons8.com/ios/35/null/rook.png"/>
        if (newValue === 'r') return <img src="https://img.icons8.com/ios-filled/35/null/rook.png"/>
        if (newValue === 'N') return <img src="https://img.icons8.com/ios/35/null/knight.png"/>
        if (newValue === 'n') return <img src="https://img.icons8.com/ios-filled/35/null/knight.png"/>
        if (newValue === 'B') return <img src="https://img.icons8.com/ios/35/null/bishop.png"/>
        if (newValue === 'b') return <img src="https://img.icons8.com/ios-filled/35/null/bishop.png"/>
        if (newValue === 'Q') return <img src="https://img.icons8.com/ios/35/null/queen.png"/>
        if (newValue === 'q') return <img src="https://img.icons8.com/ios-filled/35/null/queen.png"/>
        if (newValue === 'K') return <img src="https://img.icons8.com/ios/35/null/king.png"/>
        if (newValue === 'k') return <img src="https://img.icons8.com/ios-filled/35/null/king.png"/>

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
            <Typography variant={variant}>
                {newValue} 
            </Typography>
        
    </Button>
    );
  }