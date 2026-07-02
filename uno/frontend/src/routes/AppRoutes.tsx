import { createHashRouter } from 'react-router'
import App from '../App'
import Home from '../pages/Home'
import Sobre from '../pages/Sobre'

const router = createHashRouter([
  {
    path: '/',
    element: <App />,
    children: [
      { index: true, element: <Home /> },
      { path: 'sobre', element: <Sobre /> },
    ],
  },
])

export default router