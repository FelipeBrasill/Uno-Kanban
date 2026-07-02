import { createHashRouter } from 'react-router'
import App from '../App'
import Home from '../pages/Home'
import Sobre from '../pages/Sobre'
import Login from '../pages/Login'

const router = createHashRouter([
  {
    path: '/',
    element: <App />,
    children: [
      { index: true, element: <Login /> },
      { path: 'sobre', element: <Sobre /> },
      { path: 'home', element: <Home /> },
    ],
  },
])

export default router