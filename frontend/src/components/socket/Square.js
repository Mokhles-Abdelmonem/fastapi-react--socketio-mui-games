import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';


export default function Square({ value, onSquareClick }) {
    
    const style={
        fontSize: 30,
        borderRadius: 0,
        maxWidth: '140px',
        maxHeight: '140px',
        minWidth: '140px',
        minHeight: '140px'
    }
    
    const color = value === 'X' ? 'primary' :
    value === 'O' ? 'error' : 'info';
    
    
    return (
    <Button variant="contained" style={style}
        color={color}
        onClick={onSquareClick}>
            <Typography variant="h2">
                {value} 
            </Typography>
        
    </Button>
    );
  }