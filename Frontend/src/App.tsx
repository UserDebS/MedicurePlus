import { BrowserRouter, Routes, Route } from 'react-router-dom';
import './App.css'
import Layout from './components/Layout';
import Auth from './Screens/Auth';
import Home from './Screens/Home';
import FocusedHome from './Screens/FocusedHome';
import Register from './Screens/Register';
import Orders from './Screens/Orders';



function App() {
  return (
    <BrowserRouter>
        <Routes>
          <Route path='/' element={<Layout />}>
            <Route index path='/' element={<Auth />} />
            <Route path='signup' element={<Register />} />
            <Route path='home' element={<Home />} />
            <Route path='home/:id' element={<FocusedHome />} />
            <Route path='history' element={<Orders />} />
            <Route path='*' element={<>Error</>} />
          </Route>
        </Routes>
    </BrowserRouter>
  )
}

export default App
