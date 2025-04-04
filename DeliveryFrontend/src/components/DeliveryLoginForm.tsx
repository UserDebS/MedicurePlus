import { toast } from "sonner";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import apiFetcher from "../lib/apiFetcher";
import { useState } from "react";
import { useAuth } from "../lib/authContext";

const DeliveryLoginForm = () => {
    const [email, setEmail] = useState<string>('');
    const [password, setPassword] = useState<string>('');

    const {setDeliveryValidationTrue} = useAuth();

    const handleSubmit : React.FormEventHandler<HTMLFormElement> = (event) => {
        event.preventDefault();

        if(email === '' || password === '') {
            toast(
                <span className="font-bold text-red-500">
                    Fields aren't set properly!
                </span>
            );
            return;
        }

        apiFetcher.authByDeliveryId({
            email : email,
            password : password
        }).then(res => res.json())
        .then(res => {
            if(res.status === 200) {
                toast(
                    <span className="font-bold text-green-500">
                        Login successful!
                    </span>
                );
                //Navigation will be handled by Auth.tsx
                setDeliveryValidationTrue();
            } else {
                console.log(res);
                toast(<span className="font-bold text-red-500">
                    Account doesn't exist!
                </span>);
            }
        })
        .catch(_ => {
            toast(<span className="font-bold text-red-500">
                Account doesn't exist!
            </span>);
        });
    }

    return (
        <form className="h-full w-full p-2" onSubmit={handleSubmit}>
            <h1 className="font-bold text-4xl text-white">Login as a delivery person</h1>
            <label className="font-bold">
                Email
                <Input
                value={email}
                onChange={(e) => {
                    setEmail(e.target.value);
                }}
                className="w-1/2 bg-white" type="email" required/>
            </label>
            <label className="font-bold">
                Password
                <Input
                value={password}
                onChange={(e) => {
                    setPassword(e.target.value);
                }}
                className="w-1/2 bg-white" type="password" required/>
            </label>
            <br />
            <Button type="submit">Login</Button>
        </form>
    );
}
 
export default DeliveryLoginForm;