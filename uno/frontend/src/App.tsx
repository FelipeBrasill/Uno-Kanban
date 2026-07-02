import { Outlet, useLocation } from 'react-router'
import Banner from './components/Banner'

function App() {
  const location = useLocation()
  const esconderBanner = location.pathname === '/'

  return (
    <div>
      { !esconderBanner && <Banner /> }
      <Outlet />
    </div>
  )
}

export default App