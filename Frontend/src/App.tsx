import React, { useEffect, useState } from 'react';
import './App.css'
import { Button } from './components/ui/button';

function App() {
  const [imageInput, setImageInput] = useState<File | null>(null);

  // useEffect(() => {
  //     fetch('http://127.0.0.1:5500/suggestion?suggestion=a').then(async(res) => console.log(await res.json()));
  // }, [])

  const toBase64 = async () => {
      return new Promise((resolve, reject) => {
        const filereader = new FileReader()
        filereader.readAsDataURL(imageInput!)
        filereader.onload = () => {
            resolve(filereader.result)
        }
        filereader.onerror = reject;
      })
  }

  const handleSubmit = async(e: React.FormEvent) => {
    e.preventDefault();
    if(imageInput == null) return;
    const base64str = await toBase64().then(res => res as string).catch(_ => 'blank');
    if(base64str === 'blank') return;
    console.log(await (fetch('http://127.0.0.1:5500/upload', {
      method : 'POST',
      headers : {
        'Content-type' : 'application/json'
      },
      credentials : 'include',
      body : JSON.stringify({"image" : base64str})
    }).then(res => res.json())))
  }

  const imageChange : React.ChangeEventHandler<HTMLInputElement> = async(e) => { 
      const files = e.currentTarget.files as FileList
      if(files?.length) {
        console.log('File has values')
        setImageInput(files?.[0])
      }
  }

  const printer = () => {
    console.log(imageInput);
  }

  return (
    <form onSubmit={handleSubmit}>
      <input type="file" accept='image/*' name="image" id="image" onChange={e => imageChange(e)} />
      <Button onClick={_ => printer()}>Printer</Button>
      <Button type="submit">Submit</Button>
    </form>
  )
}

export default App
