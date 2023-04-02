import {
    REGISTER_SUCCESS,
    REGISTER_FAIL,
    SET_AUTH_LOADING,
    REMOVE_AUTH_LOADING,
} from './types';
const API_URL = process.env.REACT_APP_API_URL;




export const register = (
    username,
    email,
    password
) => async dispatch => {
    const body = JSON.stringify({
        username,
        email,
        password
    });
    dispatch({
        type: SET_AUTH_LOADING
    });

    try {    

        const apiRes = await fetch(`${API_URL}/register/`, {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: body
        });
        if (apiRes.status === 200) {
            dispatch({
                type: REGISTER_SUCCESS
            });
        } else {
            dispatch({
                type: REGISTER_FAIL
            });
            const res = await apiRes.json();
            return res
        }
    } catch(err) {
        dispatch({
            type: REGISTER_FAIL
        });
    }

    dispatch({
        type: REMOVE_AUTH_LOADING
    });
};