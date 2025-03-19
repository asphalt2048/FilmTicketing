import axios from 'axios'
import {jwtDecode} from "jwt-decode";

class AuthService{
    async login(user){
        return axios.post('http://127.0.0.1:8000/user/token/', {
            username: user.username,
            password: user.password
        })
            .then(response => {
                if(response.data.access){
                    localStorage.setItem('access_token', JSON.stringify(response.data.access));
                    localStorage.setItem('refresh_token', JSON.stringify(response.data.refresh));
                    localStorage.setItem('username', user.username);
                    this.get_user_id(response.data.access, user.username);
                }
                console.log('login success');
                return user.username;
            });
    }
    logout(){
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('username');
        localStorage.removeItem('user_id');
    }
    refreshToken(){
        let refreshToken = localStorage.getItem('refresh_token')
        refreshToken = JSON.parse(refreshToken)
        return axios.post('http://127.0.0.1:8000/user/token/refresh/', {refresh: refreshToken})
            .then(response => {
                localStorage.setItem('access_token', JSON.stringify(response.data.access))
                return response.data.access
            })
    }
    get_user_id(accessToken, username){
        axios.get('http://127.0.0.1:8000/user/id/', {
            params: {username: username},
            headers: { 'Authorization': 'Bearer ' + accessToken }
        }).then(response => {
            localStorage.setItem('user_id', response.data);
        }).catch(error => {
            console.log(error);
        })
    }
    is_accessToken_expired(token){
        const temp = jwtDecode(token)
        return temp.exp < Date.now()/1000
    }
}

export default new AuthService();