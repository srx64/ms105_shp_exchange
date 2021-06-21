import axios from 'axios'

const getAPI = axios.create({
    baseURL: 'http://shp-exchange.tk/',
    timeout: 1000,
})

export { getAPI }
