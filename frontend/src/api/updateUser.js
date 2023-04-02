const API_URL = process.env.REACT_APP_API_URL;


export async function updateUsers (username,level,disabled) {
    const Token = localStorage.getItem("authTokens")
    const access_token = JSON.parse(Token).access_token
    const body = JSON.stringify({
        level,
        disabled
    });

    try {
        const apiRes = await fetch(`${API_URL}/users/admin_update_users/${username}/`, {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${access_token}`
            },
            body: body
        });
        const res = await apiRes.json();
        console.log("res",res);
        if (apiRes.status === 200) {
            return res;
        } else {
            console.log('Error', apiRes.status, res);
            return apiRes.error
        }
    } catch(err) {
        return {error: 'somthing went wrong try again'};
    }


};