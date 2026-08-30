import axios from 'axios'

const api = axios.create({
  baseURL: '/api/proxy',
})

export default api