import axios from "axios"
let production = process.env.NODE_ENV == "production";
const api = axios.create({
    baseURL: (production ? "" : ("http://" + window.location.hostname + ":5000") ) + "/api/",
    withCredentials: !production
})
api.interceptors.response.use(response=>response.data,error=>{throw error});
export default api