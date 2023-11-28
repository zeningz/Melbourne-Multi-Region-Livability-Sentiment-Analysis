import _axios from "axios";

// get the back end url 
const axios = baseURL =>{
    const instance = _axios.create({
        baseURL: "http://172.26.131.98:8888/"
    })
    return instance
}

export {axios}

export default axios();