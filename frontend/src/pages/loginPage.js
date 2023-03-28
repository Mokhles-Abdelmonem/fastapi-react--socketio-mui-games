import React, { useState, useEffect, useContext } from 'react';
import AuthContext from '../context/AuthContext'
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import FormControlLabel from '@mui/material/FormControlLabel';
import Checkbox from '@mui/material/Checkbox';
import Link from '@mui/material/Link';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import { useHistory } from "react-router-dom";


import { Formik, Form, Field } from 'formik';
import { TextField } from 'formik-mui';
import Alert from '@mui/material/Alert';
import { loginSchema } from '../schemas/index';


const theme = createTheme();




export default function LoginPage() {
  const [alertData, setAlertData] = useState("");
  const history = useHistory();
  const { user, loginUser } = useContext(AuthContext);
  if (user) history.push("/");
  const onSubmit = async (values, actions) => {
    await new Promise((resolve) => setTimeout(resolve, 1000));
    actions.resetForm();
    const username = values.username;
    const password = values.password;
    if (username.length > 0) {
        loginUser(username, password).then((res) => {
            if (res) setAlertData(res.detail);
          });
    }
  };

  return (
    <ThemeProvider theme={theme}>
        <Box
          sx={{
            marginTop: 8,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            borderColor: 'error.main',
            borderRadius: '16px',
          }}
          >
        <Container component="main" maxWidth="xs"
        sx={{borderColor: 'error.main',}}
        >
          <CssBaseline />
          <Box
            sx={{
              marginTop: 8,
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
            }}
          >
            <Avatar sx={{ m: 1, bgcolor: 'secondary.main' }}>
              <LockOutlinedIcon />
            </Avatar>
            <Typography component="h1" variant="h5">
              Sign in
            </Typography>
              <Formik
                initialValues={{ username: "", password: "" }}
                validationSchema={loginSchema}
                onSubmit={onSubmit}
              >
                    {({ isSubmitting }) => (
                <Form>
                  {
                  alertData &&
                  <Alert severity="error">
                    {alertData}
                  </Alert>
                  }
                <Field
                  component={TextField}
                  type="username"
                  margin="normal"
                  fullWidth
                  id="username"
                  label="username"
                  name="username"
                  autoFocus
                />
                <Field
                  component={TextField}
                  margin="normal"
                  fullWidth
                  name="password"
                  label="Password"
                  type="password"
                  id="password"
                />
                <FormControlLabel
                  control={<Checkbox value="remember" color="primary" />}
                  label="Remember me"
                />
                <Button
                  type="submit"
                  fullWidth
                  variant="contained"
                  sx={{ mt: 3, mb: 2 }}
                  disabled={isSubmitting}
                >
                  Sign In
                </Button>
                <Grid container>
                  <Grid item xs>
                    <Link href="#" variant="body2">
                      Forgot password?
                    </Link>
                  </Grid>
                  <Grid item>
                    <Link href="/register" variant="body2">
                      {"Don't have an account? Sign Up"}
                    </Link>
                  </Grid>
                </Grid>
                </Form>
                )}
              </Formik>
          </Box>
        </Container>
        </Box>
    </ThemeProvider>
  );
}