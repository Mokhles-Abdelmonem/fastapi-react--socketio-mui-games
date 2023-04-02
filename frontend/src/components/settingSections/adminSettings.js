import * as React from 'react';
import Button from '@mui/material/Button';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import CircularProgress from '@mui/material/CircularProgress';
import { useState } from 'react';
import { Formik, Form, Field } from 'formik';
import { updateUserSchema } from "../../schemas";
import { TextField } from 'formik-mui';
import Alert from '@mui/material/Alert';
import { updateUsers } from '../../api/updateUser';
import { deleteUser } from '../../api/deleteUser';


export default function AdminSettings ({selectedPlayer}) {


    const initialState = {
      level: '',
      toggle: false,
      success: '',
      error: '',
    };

    const [alertData, setAlertData] = useState(initialState);
        
    const {
        level,
        toggle,
        success,
        error,
    } = alertData;

    const handleDeletePlayer = async function(){
      document.getElementById(`${selectedPlayer}`).disabled = true;
      console.log('delete player clicked')
      deleteUser(selectedPlayer).then((res) => {
        setAlertData(alertData =>({...alertData,...res,}))
      })
      window.location.reload();
    };
    const onSubmit = async (values, actions) => {
      console.log("values submitted to Admin", selectedPlayer, values);
      await new Promise((resolve) => setTimeout(resolve, 1000));
      actions.resetForm();
      
      setAlertData({...initialState})
      
      updateUsers(selectedPlayer, parseInt(values.level), values.toggle)
      .then((res) => setAlertData(alertData =>({...alertData,...res,})
      ));
  }

    {success && console.log(success);}
    return (
      <>
      {selectedPlayer ?
        (
          <Box
          sx={{
            marginTop: 8,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
          }}
        >
          <Formik
          initialValues={{ 
            level: '',
            toggle: false,
          }}
          validationSchema={updateUserSchema}
          onSubmit={onSubmit}
          >
            {({ isSubmitting }) => (
              <Form>
                <Grid container spacing={2}>
                  <Grid item xs={12}>
                    <Field
                      component={TextField}
                      autoComplete="given-name"
                      name="level"
                      fullWidth
                      id="level"
                      label="player level"
                      autoFocus
                    />
                  </Grid>
    
                  <Grid item xs={12}>
                    <label> 
                    <Field 
                     type="checkbox"
                     name="toggle" 
                     />
                      disable player
                    </label>
                  </Grid>
                </Grid>

                  <Button
                    type="submit"
                    fullWidth
                    variant="contained"
                    sx={{ mt: 3, mb: 2 }}
                    disabled={isSubmitting}
                  >
                    update
                  </Button>
    
                {
                  success && 
                  <Alert severity="success" color="info">
                    {success}
                  </Alert>
                }
                
                {
                  error && 
                  <Alert severity="error">
                    {error}
                  </Alert>
                }
    
              </Form>
              )}
              
            </Formik>
                <Button
                type="submit"
                variant="contained"
                color='error'
                id={selectedPlayer}
                sx={{ mt: 3, mb: 1 }}
                onClick={handleDeletePlayer}
                >
                  delete {selectedPlayer}
                </Button>
          </Box>
        ):
        (
          ''
        )
      }
      </>


    );
  
};

