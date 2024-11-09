import { useState } from 'react'
import './App.css'

function App() {
  const [image, setImage] = useState(null);
  const imageChange = (event : any) => {
      console.log(event.target.files[0])
      setImage(event.target.files[0]);
  }
  const handleSubmit = (e : React.FormEvent<HTMLFormElement>) => {
      e.preventDefault();
      const formdata = new FormData();
      formdata.append('image', image!);
      console.log(formdata)
  }
  return (
    <>
      <form onSubmit={handleSubmit}>
        <input className='text-3xl' type="file" accept='image/*' onChange={imageChange}/>
        <button type="submit">Submit</button>
      </form>
    </>
  )
}

export default App
