
const API_URL = process.env.REACT_APP_API_URL;




export async function get_users() {
    const Token = localStorage.getItem("authTokens")
    const access_token = JSON.parse(Token).access_token
    try {
        const res = await fetch(`${API_URL}/users/`, {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
                'Authorization': `Bearer ${access_token}`
            }
        });

        const data = await res.json();
        if (res.status === 200) {
            return data;
        } else {
            return res.error
        }
    } catch(err) {
        return {error: 'Something went wrong when retrieving users'}
    }
};