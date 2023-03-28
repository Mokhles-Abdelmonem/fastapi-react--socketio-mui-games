import * as React from 'react';
import Button from '@mui/material/Button';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import CircularProgress from '@mui/material/CircularProgress';
import { useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { updateProfille } from '../../actions/auth/updateProfile';
import { Formik, Form, Field } from 'formik';
import { profileSchema } from "../../schemas";
import { TextField } from 'formik-mui';
import Alert from '@mui/material/Alert';


const AcountSettings = () => {
  
    const user = useSelector(state => state.auth.user);
    const dispatch = useDispatch();
    const loading = useSelector(state => state.auth.loading);

    const initialState = {
      first_name: '',
      last_name: '',
      email: '',
      success: '',
      error: '',
    };

    const [alertData, setAlertData] = useState(initialState);
        
    const {
        first_name,
        last_name,
        email,
        success,
        error,
    } = alertData;


    const onSubmit = async (values, actions) => {

      await new Promise((resolve) => setTimeout(resolve, 1000));
      actions.resetForm();

      setAlertData({...initialState})
      
      if (dispatch && dispatch !== null && dispatch !== undefined){
      dispatch(updateProfille(values.email, values.first_name, values.last_name))
      .then((res) => setAlertData(alertData =>({...alertData,...res,})
      ));
    }
  }

    {email && console.log(email);}
    {success && console.log(success);}
    return (
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
        first_name: '',
        last_name: '',
        email: '',
      }}
      validationSchema={profileSchema}
      onSubmit={onSubmit}
      >
        {({ isSubmitting }) => (
          <Form>
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <Field
                  component={TextField}
                  autoComplete="given-name"
                  name="first_name"
                  fullWidth
                  id="first_name"
                  label="First Name"
                  autoFocus
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <Field
                  component={TextField}
                  fullWidth
                  id="last_name"
                  label="Last Name"
                  name="last_name"
                  autoComplete="family-name"

                />
              </Grid>
              {
              first_name &&
              <Grid item xs={12}>
              <Alert severity="error">
                {first_name}
              </Alert>
              </Grid>
              }
              {
                last_name &&
              <Grid item xs={12}>
              <Alert severity="error">
                {last_name}
              </Alert>
              </Grid>
              }
              <Grid item xs={12}>
                <Field
                  component={TextField}
                  fullWidth
                  id="email"
                  label="Email Address"
                  name="email"
                  autoComplete="email"
                />
              </Grid>
              {
              email &&
              <Grid item xs={12}>
              <Alert severity="error">
                {email}
              </Alert>
              </Grid>
              }
            </Grid>
            {
              loading ? (
              <CircularProgress />
              ) : (
              <Button
                type="submit"
                fullWidth
                variant="contained"
                sx={{ mt: 3, mb: 2 }}
                disabled={isSubmitting}
              >
                Save
              </Button>
              )
            }

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
      </Box>

    );
  
};

export default AcountSettings;