import { Outlet, useLocation } from 'react-router'
import Banner from './components/Banner'

function App() {
  const location = useLocation()
  const esconderBanner = location.pathname === '/login'

  return (
    <div className="flex flex-col min-h-screen">
      {!esconderBanner && <Banner />}

      <div className="flex flex-col flex-1">
        <Outlet />
      </div>
    </div>
  )
}

export default App