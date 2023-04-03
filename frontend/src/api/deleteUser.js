
const API_URL = process.env.REACT_APP_API_URL;


export async function deleteUser (username) {
    const Token = localStorage.getItem("authTokens")
    const access_token = JSON.parse(Token).access_token
    try {
        const apiRes = await fetch(`${API_URL}/users/admin_delete_users/${username}/`, {
            method: 'DELETE',
            headers: {
                'Accept': 'application/json',
                'Authorization': `Bearer ${access_token}`
            },
        });
        const res = await apiRes.json();
        if (apiRes.status === 200) {
            return res;
        } else {
            return apiRes.error
        }
    } catch(err) {
        return {error: 'somthing went wrong try again'};
    }


};