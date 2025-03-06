import {BrowserRouter, Routes, Route} from 'react-router-dom';
import Layout from './components/Layout';
import ShopHome from './Screens/ShopHome';
import Auth from './Screens/Auth';
import DeliveryHome from './Screens/DeliveryHome';
import Error from './Screens/Error';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<Layout />}>
          <Route index element={<Auth />}/>
          <Route path='shops/home' element={<ShopHome />}/>
          <Route path='deliveries/home' element={<DeliveryHome />}/>
          <Route path='*' element={<Error />}/>
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
